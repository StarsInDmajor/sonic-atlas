#!/usr/bin/env python3
"""
Test sparse reconstruction strategies v3.
Fixed STFT overlap-add + new strategies.
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
# 1. Global FFT top-K
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
# 2. STFT with correct COLA reconstruction
# Uses analysis-modify-synthesis with hop = win_size/2 (COLA for Hann)
# ============================================================================
def stft_topk(sig, K, win_size=1024):
    """STFT top-K with proper COLA overlap-add (hop = win_size/2)."""
    n = len(sig)
    hop = win_size // 2  # COLA with Hann window
    window = np.hanning(win_size)
    n_frames = max(1, (n - win_size) // hop + 1)
    n_freq = win_size // 2 + 1

    # Pad signal to exact frame boundaries
    padded_len = (n_frames - 1) * hop + win_size
    padded = np.zeros(padded_len)
    padded[:n] = sig

    # Forward STFT
    spectra = []
    for i in range(n_frames):
        start = i * hop
        frame = padded[start:start+win_size] * window
        spectra.append(np.fft.rfft(frame, n=win_size))

    # Collect all coefficients
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

    # Synthesis: zero non-selected, iFFT, overlap-add
    recon_padded = np.zeros(padded_len)
    window_sum = np.zeros(padded_len)
    for fi in range(n_frames):
        spec = spectra[fi]
        new_spec = np.zeros_like(spec)
        for freq_i in range(len(spec)):
            if (fi, freq_i) in selected:
                new_spec[freq_i] = spec[freq_i]
        frame_recon = np.fft.irfft(new_spec, n=win_size)
        start = fi * hop
        recon_padded[start:start+win_size] += frame_recon * window
        window_sum[start:start+win_size] += window ** 2

    # Normalize
    mask = window_sum > 1e-10
    recon_padded[mask] /= window_sum[mask]
    return recon_padded[:n]

# ============================================================================
# 3. Multi-resolution: best blend of 3 STFT scales
# ============================================================================
def multires_stft(sig, K):
    """Blend STFT at 3 window sizes, allocate K by quality."""
    win_sizes = [256, 1024, 4096]
    # Equal split for simplicity
    K_per = [K // 3, K // 3, K - 2 * (K // 3)]
    
    recons = []
    for ws, k in zip(win_sizes, K_per):
        try:
            r = stft_topk(sig, k, win_size=ws)
            recons.append(r)
        except:
            recons.append(np.zeros_like(sig))
    
    # Per-sample blend: pick the one with lowest local error
    n = len(sig)
    recon = np.zeros(n)
    block = 512
    for i in range(0, n - block, block):
        seg = sig[i:i+block]
        best_err = float('inf')
        best_r = recons[0][i:i+block]
        for r in recons:
            err = np.sum((seg - r[i:i+block])**2)
            if err < best_err:
                best_err = err
                best_r = r[i:i+block]
        recon[i:i+block] = best_r
    return recon

# ============================================================================
# 4. FFT + Gabor hybrid
# ============================================================================
def fft_gabor_hybrid(sig, K):
    """Use FFT for tonal content (K*0.7), Gabor OMP for residual (K*0.3)."""
    n = len(sig)
    K_fft = max(1, int(K * 0.7))
    K_gabor = max(1, K - K_fft)
    
    # FFT part
    recon_fft = global_fft(sig, K_fft)
    residual = sig - recon_fft
    
    # Gabor OMP on residual
    t_arr = np.arange(n) / SR
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
    G = V @ V.T; d = V @ residual
    selected = []; coefs = np.zeros(V.shape[0])
    for step in range(K_gabor):
        res_dots = d - G[:, selected] @ coefs[selected] if selected else d.copy()
        for s in selected: res_dots[s] = 0
        best = int(np.argmax(np.abs(res_dots)))
        if abs(res_dots[best]) < 1e-10: break
        selected.append(best)
        sel = np.array(selected)
        try: cs = np.linalg.solve(G[np.ix_(sel, sel)], d[sel])
        except: cs = np.linalg.lstsq(G[np.ix_(sel, sel)], d[sel], rcond=None)[0]
        coefs[sel] = cs
    if selected:
        recon_gabor = V[selected].T @ coefs[selected]
    else:
        recon_gabor = np.zeros(n)
    
    return recon_fft + recon_gabor

# ============================================================================
# 5. Frequency-band splitting
# ============================================================================
def freq_band_split(sig, K):
    """Split signal into low/mid/high bands, FFT top-K in each."""
    n = len(sig)
    fc = np.fft.rfft(sig, n=n*2)
    freqs = np.fft.rfftfreq(n*2, 1/SR)
    
    # Band boundaries
    bands = [(0, 500), (500, 2000), (2000, SR/2)]
    K_per = [K // 3, K // 3, K - 2 * (K // 3)]
    
    recon = np.zeros(n)
    for (f_lo, f_hi), k in zip(bands, K_per):
        # Mask to band
        band_fc = np.zeros_like(fc)
        mask = (freqs >= f_lo) & (freqs < f_hi)
        band_fc[mask] = fc[mask]
        
        # Select top-K in band
        mags = np.abs(band_fc)
        top = np.argsort(mags)[::-1][:k]
        selected_fc = np.zeros_like(fc)
        for idx in top:
            selected_fc[idx] = band_fc[idx]
        
        recon += np.fft.irfft(selected_fc, n=n*2)[:n]
    
    return recon

# ============================================================================
# 6. Short-time sinusoidal modeling
# ============================================================================
def sinusoidal_model(sig, K, frame_size=2048, hop=512):
    """Track sinusoids across frames (like STRAHT/SMS)."""
    n = len(sig)
    n_frames = max(1, (n - frame_size) // hop + 1)
    window = np.hanning(frame_size)
    K_per_frame = max(1, K // n_frames)
    
    recon = np.zeros(n)
    window_sum = np.zeros(n)
    
    for fi in range(n_frames):
        start = fi * hop
        end = min(start + frame_size, n)
        frame = np.zeros(frame_size)
        frame[:end-start] = sig[start:end] * window[:end-start]
        
        # Find top-K sinusoids in this frame
        spec = np.fft.rfft(frame, n=frame_size)
        mags = np.abs(spec)
        phases = np.angle(spec)
        freqs = np.fft.rfftfreq(frame_size, 1/SR)
        
        top = np.argsort(mags)[::-1][:K_per_frame]
        
        # Synthesize
        frame_recon = np.zeros(frame_size)
        t_frame = np.arange(frame_size) / SR
        for idx in top:
            amp = mags[idx] / frame_size * 2
            freq = freqs[idx]
            ph = phases[idx]
            frame_recon += amp * np.cos(2*np.pi*freq*t_frame + ph)
        
        recon[start:end] += frame_recon[:end-start] * window[:end-start]
        window_sum[start:end] += window[:end-start] ** 2
    
    mask = window_sum > 1e-10
    recon[mask] /= window_sum[mask]
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
    for step in range(min(K, V.shape[0])):
        res_dots = d - G[:, selected] @ coefs[selected] if selected else d.copy()
        for s in selected: res_dots[s] = 0
        best = int(np.argmax(np.abs(res_dots)))
        if abs(res_dots[best]) < 1e-10: break
        selected.append(best)
        sel = np.array(selected)
        try: cs = np.linalg.solve(G[np.ix_(sel, sel)], d[sel])
        except: cs = np.linalg.lstsq(G[np.ix_(sel, sel)], d[sel], rcond=None)[0]
        coefs[sel] = cs
    return V[selected].T @ coefs[selected] if selected else np.zeros(n)

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
        'FFT':           global_fft,
        'STFT-256':      lambda s,K: stft_topk(s, K, win_size=256),
        'STFT-1024':     lambda s,K: stft_topk(s, K, win_size=1024),
        'STFT-4096':     lambda s,K: stft_topk(s, K, win_size=4096),
        'MultiRes':      multires_stft,
        'FFT+Gabor':     fft_gabor_hybrid,
        'FreqBand':      freq_band_split,
        'Sinusoidal':    lambda s,K: sinusoidal_model(s, K, frame_size=2048, hop=512),
        'GaborOMP':      gabor_omp,
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
