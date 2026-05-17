#!/usr/bin/env python3
"""
Test sparse reconstruction strategies v2 — fixed overlap-add, proper DCT.
Run: nix-shell -p python3Packages.numpy --run "python3 test_strategies2.py"
"""
import numpy as np
import wave, sys, json

SR = 44100; DUR = 0.6; N = int(DUR * SR)

def read_wav(path):
    w = wave.open(path, 'r')
    nch, sw, sr, nf = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
    raw = w.readframes(nf); w.close()
    if sw == 2:
        return np.frombuffer(raw, dtype=np.int16).reshape(-1, nch).mean(axis=1).astype(np.float64)/32768.0
    return np.frombuffer(raw, dtype=np.int32).reshape(-1, nch).mean(axis=1).astype(np.float64)/2147483648.0

def resid(sig, recon):
    return float(np.sum((sig - recon)**2) / max(np.sum(sig**2), 1e-15))

# ============================================================================
# 1. Global FFT top-K (correct)
# ============================================================================
def global_fft(sig, K):
    n = len(sig); fftN = 1
    while fftN < n: fftN <<= 1
    fc = np.fft.rfft(sig, n=fftN)
    mags = np.abs(fc); phases = np.angle(fc)
    top = np.argsort(mags)[::-1][:K]
    t = np.arange(n) / SR
    recon = np.zeros(n)
    for idx in top:
        freq = idx * SR / fftN
        recon += mags[idx]/n*2 * np.cos(2*np.pi*freq*t + phases[idx])
    return recon

# ============================================================================
# 2. STFT with correct overlap-add (scola method)
# ============================================================================
def stft_topk(sig, K, win_size=1024, hop=None):
    """Proper STFT: compute all frames, select top-K coefficients, reconstruct via overlap-add."""
    if hop is None: hop = win_size // 4
    n = len(sig)
    window = np.hanning(win_size)
    n_frames = max(1, (n - win_size) // hop + 1)
    n_freq = win_size // 2 + 1

    # Forward STFT
    spectra = []
    for i in range(n_frames):
        start = i * hop
        frame = sig[start:start+win_size] * window
        spectra.append(np.fft.rfft(frame))

    # Collect ALL coefficients with (frame, freq) labels and magnitudes
    coefs = []
    for fi, spec in enumerate(spectra):
        mags = np.abs(spec)
        for freq_i in range(len(mags)):
            coefs.append((mags[freq_i], fi, freq_i))
    coefs.sort(key=lambda x: -x[0])

    # Select top-K
    selected = set()
    for _, fi, freq_i in coefs[:K]:
        selected.add((fi, freq_i))

    # Reconstruct: zero out non-selected, iFFT each frame, overlap-add
    recon = np.zeros(n)
    weight = np.zeros(n)
    for fi, spec in enumerate(spectra):
        new_spec = np.zeros_like(spec)
        for freq_i in range(len(spec)):
            if (fi, freq_i) in selected:
                new_spec[freq_i] = spec[freq_i]
        frame_recon = np.fft.irfft(new_spec, n=win_size)
        start = fi * hop
        end = min(start + win_size, n)
        recon[start:end] += frame_recon[:end-start] * window[:end-start]
        weight[start:end] += window[:end-start]**2

    mask = weight > 1e-10
    recon[mask] /= weight[mask]
    return recon

# ============================================================================
# 3. Multi-resolution STFT: blend short + long
# ============================================================================
def multires_stft(sig, K):
    """Short window (256) for transients + long window (4096) for tonal, K split 30/70."""
    K_short = int(K * 0.3)
    K_long = K - K_short
    recon_s = stft_topk(sig, K_short, win_size=256, hop=64)
    recon_l = stft_topk(sig, K_long, win_size=4096, hop=1024)

    # Blend based on local energy: high-energy regions → favor short window
    n = len(sig)
    frame = 1024
    recon = np.zeros(n)
    for i in range(0, n - frame, frame):
        seg = sig[i:i+frame]
        e = np.sum(seg**2)
        # Short-window quality proxy: how well does short window match?
        err_s = np.sum((seg - recon_s[i:i+frame])**2)
        err_l = np.sum((seg - recon_l[i:i+frame])**2)
        # Weight inversely proportional to error
        w_s = 1.0 / max(err_s, 1e-15)
        w_l = 1.0 / max(err_l, 1e-15)
        total = w_s + w_l
        recon[i:i+frame] = (recon_s[i:i+frame] * w_s + recon_l[i:i+frame] * w_l) / total
    return recon

# ============================================================================
# 4. Per-harmonic tracking + decay model
# ============================================================================
def harmonic_tracking(sig, K):
    """Detect fundamental, extract harmonics with individual decay envelopes."""
    n = len(sig)
    t = np.arange(n) / SR

    # Find fundamental via autocorrelation
    min_lag = int(SR / 5000)   # 5 kHz max
    max_lag = int(SR / 50)     # 50 Hz min
    autocorr = np.correlate(sig, sig[:max_lag], mode='full')
    autocorr = autocorr[max_lag:]  # positive lags only
    peak_lag = min_lag + np.argmax(autocorr[min_lag:max_lag])
    f0 = SR / peak_lag

    # Track harmonics
    recon = np.zeros(n)
    atoms = []
    for h in range(1, K+1):
        fh = h * f0
        if fh > SR/2: break

        # Extract harmonic via bandpass (simplified: multiply by cosine and lowpass)
        # Use analytic signal approach
        analytic = sig * np.exp(-2j * np.pi * fh * t)
        # Low-pass filter (moving average)
        kernel_size = max(1, int(SR / (fh * 0.5)))
        kernel = np.ones(kernel_size) / kernel_size
        envelope_real = np.convolve(np.real(analytic), kernel, mode='same')
        envelope_imag = np.convolve(np.imag(analytic), kernel, mode='same')

        # Reconstruct this harmonic
        harmonic = 2 * (envelope_real * np.cos(2*np.pi*fh*t) - envelope_imag * np.sin(2*np.pi*fh*t))
        recon += harmonic
        atoms.append((fh, np.max(np.abs(envelope_real + 1j*envelope_imag))))

    return recon

# ============================================================================
# 5. Best-of: use the best method per K range
# ============================================================================
def best_of(sig, K):
    """Use FFT for low K, STFT for medium K, harmonic tracking for tonal."""
    if K <= 30:
        return global_fft(sig, K)
    elif K <= 100:
        # STFT with good window size
        return stft_topk(sig, K, win_size=512, hop=128)
    else:
        # Combine FFT (tonal) + STFT residual (transient)
        fft_part = global_fft(sig, min(K, 50))
        residual = sig - fft_part
        stft_part = stft_topk(residual, K - 50, win_size=256, hop=64)
        return fft_part + stft_part

# ============================================================================
# 6. STFT with perceptual weighting
# ============================================================================
def stft_perceptual(sig, K, win_size=1024, hop=None):
    """STFT top-K but weight by perceptual importance (A-weighting approximation)."""
    if hop is None: hop = win_size // 4
    n = len(sig)
    window = np.hanning(win_size)
    n_frames = max(1, (n - win_size) // hop + 1)
    n_freq = win_size // 2 + 1
    freqs = np.fft.rfftfreq(win_size, 1/SR)

    # A-weighting approximation (simplified)
    # Boost 1-4kHz, attenuate below 100Hz and above 10kHz
    a_weight = np.ones(n_freq)
    for fi in range(n_freq):
        f = freqs[fi]
        if f < 100: a_weight[fi] = 0.1
        elif f < 1000: a_weight[fi] = 0.1 + 0.9 * (f - 100) / 900
        elif f <= 4000: a_weight[fi] = 1.0
        elif f <= 10000: a_weight[fi] = 1.0 - 0.5 * (f - 4000) / 6000
        else: a_weight[fi] = 0.5

    # Forward STFT
    spectra = []
    for i in range(n_frames):
        start = i * hop
        frame = sig[start:start+win_size] * window
        spectra.append(np.fft.rfft(frame))

    # Collect coefficients weighted by perception
    coefs = []
    for fi, spec in enumerate(spectra):
        mags = np.abs(spec)
        for freq_i in range(len(mags)):
            weighted_mag = mags[freq_i] * a_weight[freq_i]
            coefs.append((weighted_mag, fi, freq_i))
    coefs.sort(key=lambda x: -x[0])

    selected = set()
    for _, fi, freq_i in coefs[:K]:
        selected.add((fi, freq_i))

    recon = np.zeros(n)
    weight = np.zeros(n)
    for fi, spec in enumerate(spectra):
        new_spec = np.zeros_like(spec)
        for freq_i in range(len(spec)):
            if (fi, freq_i) in selected:
                new_spec[freq_i] = spec[freq_i]
        frame_recon = np.fft.irfft(new_spec, n=win_size)
        start = fi * hop
        end = min(start + win_size, n)
        recon[start:end] += frame_recon[:end-start] * window[:end-start]
        weight[start:end] += window[:end-start]**2
    mask = weight > 1e-10
    recon[mask] /= weight[mask]
    return recon

# ============================================================================
# 7. Gabor OMP (reference)
# ============================================================================
def gabor_omp(sig, K):
    n = len(sig); t_arr = np.arange(n) / SR
    T0S = [0.01, 0.06, 0.15, 0.3, 0.5]
    F0S = [130, 196, 262, 440, 700, 1100, 1760, 2800, 4400]
    SIGMAS = [0.005, 0.02, 0.08, 0.25]
    vecs = []
    for t0 in T0S:
        for f0 in F0S:
            for sigma in SIGMAS:
                v = np.exp(-((t_arr-t0)**2)/(2*sigma**2)) * np.cos(2*np.pi*f0*(t_arr-t0))
                nm = np.linalg.norm(v)
                if nm > 1e-10: v /= nm
                vecs.append(v)
    V = np.array(vecs)
    G = V @ V.T; d = V @ sig
    selected = []; coefs = np.zeros(V.shape[0])
    for step in range(K):
        res_dots = d - G[:, selected] @ coefs[selected] if selected else d.copy()
        for s in selected: res_dots[s] = 0
        best = int(np.argmax(np.abs(res_dots)))
        if abs(res_dots[best]) < 1e-10: break
        selected.append(best)
        sel = np.array(selected)
        try: cs = np.linalg.solve(G[np.ix_(sel, sel)], d[sel])
        except: cs = np.linalg.lstsq(G[np.ix_(sel, sel)], d[sel], rcond=None)[0]
        coefs[sel] = cs
    return V[selected].T @ coefs[selected]

# ============================================================================
# Main
# ============================================================================
def main():
    piano = read_wav('/tmp/piano_c4.wav')[:N]
    guitar = read_wav('/tmp/guitar_c4.wav')[:N]
    def norm(s):
        mx = np.max(np.abs(s))
        return s * 0.9 / mx if mx > 0 else s

    signals = {'piano': norm(piano), 'guitar': norm(guitar)}
    strategies = {
        'FFT':         global_fft,
        'STFT-256':    lambda s,K: stft_topk(s, K, win_size=256, hop=64),
        'STFT-512':    lambda s,K: stft_topk(s, K, win_size=512, hop=128),
        'STFT-1024':   lambda s,K: stft_topk(s, K, win_size=1024, hop=256),
        'STFT-4096':   lambda s,K: stft_topk(s, K, win_size=4096, hop=1024),
        'MultiRes':    multires_stft,
        'Harmonic':    harmonic_tracking,
        'BestOf':      best_of,
        'Perceptual':  lambda s,K: stft_perceptual(s, K, win_size=1024, hop=256),
        'GaborOMP':    gabor_omp,
    }
    Ks = [5, 10, 20, 50, 100, 200]
    results = {}
    for sn, sig in signals.items():
        print(f"\n=== {sn} ===", file=sys.stderr)
        results[sn] = {}
        for name, fn in strategies.items():
            print(f"  {name}:", file=sys.stderr, end='')
            vals = []
            for K in Ks:
                try:
                    recon = fn(sig, K)
                    r = resid(sig, recon)
                    vals.append((K, round(r, 6)))
                    print(f" {K}→{r*100:.1f}%", file=sys.stderr, end='')
                except Exception as e:
                    vals.append((K, None))
                    print(f" {K}→ERR", file=sys.stderr, end='')
            results[sn][name] = vals
            print(file=sys.stderr)
    print(json.dumps(results, separators=(',', ':')))

if __name__ == '__main__':
    main()
