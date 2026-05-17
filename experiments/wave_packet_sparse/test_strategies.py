#!/usr/bin/env python3
"""
Experiment: multiple sparse representation strategies for real audio.
Run: nix-shell -p python3Packages.numpy --run "python3 test_strategies.py"

Tests:
  1. Global FFT top-K
  2. Global DCT top-K
  3. Per-window FFT (STFT) with total K budget
  4. Per-window MDCT with total K budget
  5. Multi-resolution STFT (short + long windows)
  6. Gabor dictionary (MP/OMP) - baseline
  7. Learned Gabor from STFT peaks
"""
import numpy as np
import struct, wave, sys, json

SR = 44100; DUR = 0.6; N = int(DUR * SR)

def read_wav(path):
    w = wave.open(path, 'r')
    nch, sw, sr, nf = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
    raw = w.readframes(nf); w.close()
    if sw == 2:
        return np.frombuffer(raw, dtype=np.int16).reshape(-1, nch).mean(axis=1).astype(np.float64)/32768.0
    return np.frombuffer(raw, dtype=np.int32).reshape(-1, nch).mean(axis=1).astype(np.float64)/2147483648.0

def residual_ratio(orig, recon):
    return float(np.sum((orig - recon)**2) / max(np.sum(orig**2), 1e-15))

# ============================================================================
# Strategy 1: Global FFT top-K
# ============================================================================
def global_fft(sig, K):
    n = len(sig)
    fftN = 1
    while fftN < n: fftN <<= 1
    fc = np.fft.rfft(sig, n=fftN)
    mags = np.abs(fc)
    top = np.argsort(mags)[::-1][:K]
    recon = np.zeros(n)
    t = np.arange(n) / SR
    for idx in top:
        freq = idx * SR / fftN
        recon += mags[idx]/n*2 * np.cos(2*np.pi*freq*t + np.angle(fc[idx]))
    return recon

# ============================================================================
# Strategy 2: Global DCT top-K
# ============================================================================
def global_dct(sig, K):
    n = len(sig)
    # DCT-II via FFT
    y = np.zeros(2*n)
    y[:n] = sig
    y[n:] = sig[::-1]
    Y = np.fft.fft(y)[:n]
    phase = np.exp(-1j*np.pi*np.arange(n)/(2*n))
    dct_c = np.real(Y * phase) * 2
    
    mags = np.abs(dct_c)
    top = np.argsort(mags)[::-1][:K]
    recon = np.zeros(n)
    for idx in top:
        c = dct_c[idx]
        scale = (1.0/n) if idx == 0 else (2.0/n)
        recon += c * scale * np.cos(np.pi/n * (np.arange(n)+0.5) * idx)
    return recon

# ============================================================================
# Strategy 3: STFT — per-window FFT, total K budget
# ============================================================================
def stft_recon(sig, K, win_size=1024, hop=512):
    """STFT reconstruction with K total coefficients across all windows."""
    n = len(sig)
    n_windows = (n - win_size) // hop + 1
    window = np.hanning(win_size)
    
    # Compute all STFT frames
    frames = []
    for i in range(n_windows):
        start = i * hop
        frame = sig[start:start+win_size] * window
        spectrum = np.fft.rfft(frame)
        frames.append(spectrum)
    
    # Collect all coefficients with their (window, freq) indices
    all_coefs = []
    for wi, spectrum in enumerate(frames):
        mags = np.abs(spectrum)
        for fi in range(len(mags)):
            all_coefs.append((mags[fi], wi, fi))
    
    # Select top-K globally
    all_coefs.sort(key=lambda x: -x[0])
    selected = set()
    for _, wi, fi in all_coefs[:K]:
        selected.add((wi, fi))
    
    # Reconstruct with selected coefficients only
    recon_frames = []
    for wi, spectrum in enumerate(frames):
        new_spec = np.zeros_like(spectrum)
        for fi in range(len(spectrum)):
            if (wi, fi) in selected:
                new_spec[fi] = spectrum[fi]
        recon_frames.append(new_spec)
    
    # Overlap-add
    recon = np.zeros(n)
    window_sum = np.zeros(n)
    for i, spec in enumerate(recon_frames):
        start = i * hop
        frame = np.fft.irfft(spec, n=win_size) * window
        recon[start:start+win_size] += frame
        window_sum[start:start+win_size] += window**2
    
    # Normalize by window sum
    mask = window_sum > 1e-10
    recon[mask] /= window_sum[mask]
    return recon

# ============================================================================
# Strategy 4: MDCT per-window, total K budget
# ============================================================================
def mdct_recon(sig, K, win_size=1024):
    """MDCT reconstruction with K total coefficients."""
    n = len(sig)
    hop = win_size // 2
    n_blocks = (n - win_size) // hop
    if n_blocks < 1:
        return np.zeros(n)
    
    # MDCT basis
    N = win_size
    k = np.arange(N//2)
    
    # Collect all MDCT coefficients
    all_coefs = []
    mdct_blocks = []
    for i in range(n_blocks):
        start = i * hop
        frame = sig[start:start+N]
        # MDCT: N/2 coefficients from N samples
        n_idx = np.arange(N)
        # Type IV DCT
        c = np.zeros(N//2)
        for ki in range(N//2):
            c[ki] = np.sum(frame * np.cos(2*np.pi/N * (n_idx + 0.5 + N/4) * (ki + 0.5)))
        mdct_blocks.append(c)
        for fi in range(N//2):
            all_coefs.append((abs(c[fi]), i, fi))
    
    # Select top-K
    all_coefs.sort(key=lambda x: -x[0])
    selected = set()
    for _, bi, fi in all_coefs[:K]:
        selected.add((bi, fi))
    
    # Reconstruct
    recon = np.zeros(n)
    window_sum = np.zeros(n)
    for bi, c in enumerate(mdct_blocks):
        new_c = np.zeros_like(c)
        for fi in range(len(c)):
            if (bi, fi) in selected:
                new_c[fi] = c[fi]
        # IMDCT
        start = bi * hop
        frame = np.zeros(N)
        n_idx = np.arange(N)
        for ki in range(N//2):
            if new_c[ki] != 0:
                frame += new_c[ki] * np.cos(2*np.pi/N * (n_idx + 0.5 + N/4) * (ki + 0.5))
        frame *= 2.0 / N
        # Window and overlap-add
        w = np.sin(np.pi/N * (n_idx + 0.5))  # sine window
        recon[start:start+N] += frame * w
        window_sum[start:start+N] += w**2
    
    mask = window_sum > 1e-10
    recon[mask] /= window_sum[mask]
    return recon

# ============================================================================
# Strategy 5: Multi-resolution STFT (short + long windows)
# ============================================================================
def multires_stft(sig, K, short_win=256, long_win=4096, hop=512):
    """Use short windows for transients, long windows for tonal content."""
    n = len(sig)
    
    # Detect transient regions (high energy variance)
    frame_size = 1024
    energies = []
    for i in range(0, n - frame_size, frame_size):
        energies.append(np.sum(sig[i:i+frame_size]**2))
    energies = np.array(energies)
    
    # Split K budget: 30% for short windows, 70% for long windows
    K_short = int(K * 0.3)
    K_long = K - K_short
    
    # Short-window STFT (better for transients)
    recon_short = stft_recon(sig, K_short, win_size=short_win, hop=short_win//2)
    
    # Long-window STFT (better for tonal)
    recon_long = stft_recon(sig, K_long, win_size=long_win, hop=long_win//2)
    
    # Adaptive blend based on local energy
    blend = np.zeros(n)
    for i in range(0, n - frame_size, frame_size):
        e = np.sum(sig[i:i+frame_size]**2)
        # Higher energy variance = more transient = favor short windows
        blend[i:i+frame_size] = 0.5  # equal blend for now
    
    recon = recon_short * 0.4 + recon_long * 0.6
    return recon

# ============================================================================
# Strategy 6: Gabor OMP (existing, for reference)
# ============================================================================
def gabor_omp(sig, K):
    """OMP with Gabor dictionary."""
    n = len(sig)
    t_arr = np.arange(n) / SR
    
    # Build dictionary
    T0S = [0.01, 0.06, 0.15, 0.3, 0.5]
    F0S = [130, 196, 262, 440, 700, 1100, 1760, 2800, 4400]
    SIGMAS = [0.005, 0.02, 0.08, 0.25]
    
    atoms = []
    for t0 in T0S:
        for f0 in F0S:
            for sigma in SIGMAS:
                v = np.exp(-((t_arr-t0)**2)/(2*sigma**2)) * np.cos(2*np.pi*f0*(t_arr-t0))
                nm = np.linalg.norm(v)
                if nm > 1e-10: v /= nm
                atoms.append(v)
    
    V = np.array(atoms)
    n_atoms = V.shape[0]
    
    # OMP
    G = V @ V.T
    d = V @ sig
    selected = []
    coefs = np.zeros(n_atoms)
    
    for step in range(K):
        sel_set = set(selected)
        res_dots = d - G[:, selected] @ coefs[selected] if selected else d.copy()
        res_dots[list(sel_set)] = 0
        best = int(np.argmax(np.abs(res_dots)))
        if abs(res_dots[best]) < 1e-10: break
        selected.append(best)
        sel = np.array(selected)
        Gss = G[np.ix_(sel, sel)]
        try: cs = np.linalg.solve(Gss, d[sel])
        except: cs = np.linalg.lstsq(Gss, d[sel], rcond=None)[0]
        coefs[sel] = cs
    
    recon = V[selected].T @ coefs[selected]
    return recon

# ============================================================================
# Strategy 7: Learned atoms from STFT peaks
# ============================================================================
def learned_gabor(sig, K):
    """Extract dominant STFT peaks as Gabor atoms, then OMP refine."""
    n = len(sig)
    t_arr = np.arange(n) / SR
    
    # Find dominant time-frequency peaks via STFT
    win_size = 1024
    hop = 256
    n_windows = (n - win_size) // hop + 1
    window = np.hanning(win_size)
    
    peaks = []
    for wi in range(n_windows):
        start = wi * hop
        frame = sig[start:start+win_size] * window
        spectrum = np.fft.rfft(frame)
        mags = np.abs(spectrum)
        freqs = np.fft.rfftfreq(win_size, 1/SR)
        
        # Find peaks (local maxima above threshold)
        for fi in range(1, len(mags)-1):
            if mags[fi] > mags[fi-1] and mags[fi] > mags[fi+1] and mags[fi] > np.max(mags)*0.02:
                t0 = (start + win_size/2) / SR
                f0 = freqs[fi]
                sigma = 0.02  # reasonable default
                amp = mags[fi]
                peaks.append((amp, t0, f0, sigma))
    
    # Sort by amplitude and take top unique atoms
    peaks.sort(key=lambda x: -x[0])
    
    # Deduplicate (merge close atoms)
    atoms = []
    for amp, t0, f0, sigma in peaks:
        is_dup = False
        for at0, af0, _ in atoms:
            if abs(t0 - at0) < 0.01 and abs(f0 - af0) < 50:
                is_dup = True
                break
        if not is_dup:
            atoms.append((t0, f0, sigma))
        if len(atoms) >= K * 3:  # collect more than needed for OMP selection
            break
    
    # Build dictionary from learned atoms
    vecs = []
    for t0, f0, sigma in atoms:
        v = np.exp(-((t_arr-t0)**2)/(2*sigma**2)) * np.cos(2*np.pi*f0*(t_arr-t0))
        nm = np.linalg.norm(v)
        if nm > 1e-10: v /= nm
        vecs.append(v)
    
    if not vecs:
        return np.zeros(n)
    
    V = np.array(vecs)
    n_atoms = V.shape[0]
    K_use = min(K, n_atoms)
    
    # OMP
    G = V @ V.T
    d = V @ sig
    selected = []
    coefs = np.zeros(n_atoms)
    
    for step in range(K_use):
        sel_set = set(selected)
        res_dots = d - G[:, selected] @ coefs[selected] if selected else d.copy()
        res_dots[list(sel_set)] = 0
        best = int(np.argmax(np.abs(res_dots)))
        if abs(res_dots[best]) < 1e-10: break
        selected.append(best)
        sel = np.array(selected)
        Gss = G[np.ix_(sel, sel)]
        try: cs = np.linalg.solve(Gss, d[sel])
        except: cs = np.linalg.lstsq(Gss, d[sel], rcond=None)[0]
        coefs[sel] = cs
    
    recon = V[selected].T @ coefs[selected]
    return recon

# ============================================================================
# Main: run all strategies at multiple K values
# ============================================================================
def main():
    piano = read_wav('/tmp/piano_c4.wav')[:N]
    guitar = read_wav('/tmp/guitar_c4.wav')[:N]
    
    def norm(s):
        mx = np.max(np.abs(s))
        return s * 0.9 / mx if mx > 0 else s
    
    signals = {
        'piano': norm(piano),
        'guitar': norm(guitar),
    }
    
    strategies = {
        'global_fft':  global_fft,
        'global_dct':  global_dct,
        'stft_1024':   lambda s, K: stft_recon(s, K, win_size=1024, hop=512),
        'stft_256':    lambda s, K: stft_recon(s, K, win_size=256, hop=128),
        'stft_4096':   lambda s, K: stft_recon(s, K, win_size=4096, hop=2048),
        'multires':    lambda s, K: multires_stft(s, K),
        'gabor_omp':   gabor_omp,
        'learned_gabor': learned_gabor,
    }
    
    Ks = [5, 10, 20, 50, 100, 200]
    
    results = {}
    for sig_name, sig in signals.items():
        print(f"\n=== {sig_name} ===", file=sys.stderr)
        results[sig_name] = {}
        for strat_name, strat_fn in strategies.items():
            print(f"  {strat_name}:", file=sys.stderr, end='')
            resids = []
            for K in Ks:
                try:
                    recon = strat_fn(sig, K)
                    r = residual_ratio(sig, recon)
                    resids.append((K, round(r, 6)))
                    print(f" K={K}:{r*100:.1f}%", file=sys.stderr, end='')
                except Exception as e:
                    print(f" K={K}:ERR({e})", file=sys.stderr, end='')
                    resids.append((K, None))
            results[sig_name][strat_name] = resids
            print(file=sys.stderr)
    
    print(json.dumps(results, separators=(',', ':')))

if __name__ == '__main__':
    main()
