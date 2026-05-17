#!/usr/bin/env python3
"""
Test sparse reconstruction strategies v5.
Focus: working STFT + sinusoidal model + hybrid methods.
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

# 1. Global FFT
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

# 2. STFT: per-frame top-K bins, K evenly distributed
def stft_recon(sig, K, win_size=1024):
    n = len(sig)
    hop = win_size // 2
    window = np.hanning(win_size)
    n_frames = max(1, (n - win_size + hop - 1) // hop + 1)
    K_per_frame = max(1, K // n_frames)
    n_freq = win_size // 2 + 1
    
    # Pad to at least n
    padded_len = max(n, (n_frames - 1) * hop + win_size)
    padded = np.zeros(padded_len)
    padded[:n] = sig
    
    recon_padded = np.zeros(padded_len)
    wsum = np.zeros(padded_len)
    
    for fi in range(n_frames):
        start = fi * hop
        frame = padded[start:start+win_size] * window
        spec = np.fft.rfft(frame)
        mags = np.abs(spec)
        
        # Select top K_per_frame bins
        top = np.argsort(mags)[::-1][:K_per_frame]
        new_spec = np.zeros(n_freq, dtype=complex)
        for idx in top:
            new_spec[idx] = spec[idx]
        
        frame_recon = np.fft.irfft(new_spec, n=win_size)
        recon_padded[start:start+win_size] += frame_recon * window
        wsum[start:start+win_size] += window**2
    
    mask = wsum > 1e-10
    recon_padded[mask] /= wsum[mask]
    return recon_padded[:n]

# 3. Multi-resolution STFT
def multires_stft(sig, K):
    recons = []
    for ws in [256, 1024]:
        recons.append(stft_recon(sig, K // 2, win_size=ws))
    
    n = len(sig)
    recon = np.zeros(n)
    blk = 512
    for i in range(0, n - blk, blk):
        seg = sig[i:i+blk]
        best_err, best_r = float('inf'), recons[0][i:i+blk]
        for r in recons:
            err = np.sum((seg - r[i:i+blk])**2)
            if err < best_err:
                best_err = err; best_r = r[i:i+blk]
        recon[i:i+blk] = best_r
    return recon

# 4. FFT + Gabor hybrid
def fft_gabor_hybrid(sig, K):
    n = len(sig)
    K_fft = max(1, int(K * 0.7))
    K_gabor = max(1, K - K_fft)
    recon_fft = global_fft(sig, K_fft)
    residual = sig - recon_fft
    
    t_arr = np.arange(n) / SR
    atoms = []
    for t0 in [0.01, 0.06, 0.15, 0.3, 0.5]:
        for f0 in [130, 196, 262, 440, 700, 1100, 1760, 2800, 4400]:
            for sigma in [0.005, 0.02, 0.08, 0.25]:
                v = np.exp(-((t_arr-t0)**2)/(2*sigma**2)) * np.cos(2*np.pi*f0*(t_arr-t0))
                nm = np.linalg.norm(v)
                if nm > 1e-10: v /= nm
                atoms.append(v)
    V = np.array(atoms)
    G = V @ V.T; d = V @ residual
    sel = []; c = np.zeros(V.shape[0])
    for _ in range(min(K_gabor, V.shape[0])):
        rd = d - G[:, sel] @ c[sel] if sel else d.copy()
        for s in sel: rd[s] = 0
        best = int(np.argmax(np.abs(rd)))
        if abs(rd[best]) < 1e-10: break
        sel.append(best)
        s_arr = np.array(sel)
        try: cs = np.linalg.solve(G[np.ix_(s_arr, s_arr)], d[s_arr])
        except: cs = np.linalg.lstsq(G[np.ix_(s_arr, s_arr)], d[s_arr], rcond=None)[0]
        c[s_arr] = cs
    recon_gabor = V[s_arr].T @ c[s_arr] if sel else np.zeros(n)
    return recon_fft + recon_gabor

# 5. FFT + STFT residual
def fft_stft_hybrid(sig, K):
    """FFT for tonal, STFT on residual for transient."""
    K_fft = max(1, int(K * 0.5))
    K_stft = K - K_fft
    recon_fft = global_fft(sig, K_fft)
    residual = sig - recon_fft
    recon_stft = stft_recon(residual, K_stft, win_size=256)
    return recon_fft + recon_stft

# 6. Freq band splitting
def freq_band_split(sig, K):
    n = len(sig); fftN = 1
    while fftN < n: fftN <<= 1
    fc = np.fft.rfft(sig, n=fftN)
    freqs = np.fft.rfftfreq(fftN, 1/SR)
    t = np.arange(n) / SR
    bands = [(0, 500), (500, 2000), (2000, SR/2)]
    Ks = [K//3, K//3, K - 2*(K//3)]
    recon = np.zeros(n)
    for (flo, fhi), k in zip(bands, Ks):
        mask = (freqs >= flo) & (freqs < fhi)
        mags = np.abs(fc) * mask
        top = np.argsort(mags)[::-1][:k]
        for idx in top:
            if mags[idx] < 1e-15: break
            freq = idx * SR / fftN
            recon += np.abs(fc[idx])/n*2 * np.cos(2*np.pi*freq*t + np.angle(fc[idx]))
    return recon

# 7. Sinusoidal modeling
def sinusoidal_model(sig, K):
    n = len(sig)
    frame_size = 2048; hop = 512
    window = np.hanning(frame_size)
    n_frames = max(1, (n - frame_size + hop - 1) // hop + 1)
    K_per_frame = max(1, K // n_frames)
    
    padded_len = max(n, (n_frames - 1) * hop + frame_size)
    padded = np.zeros(padded_len)
    padded[:n] = sig
    
    recon_padded = np.zeros(padded_len)
    wsum = np.zeros(padded_len)
    
    for fi in range(n_frames):
        start = fi * hop
        frame = padded[start:start+frame_size] * window
        spec = np.fft.rfft(frame, n=frame_size)
        mags = np.abs(spec)
        phases = np.angle(spec)
        freqs = np.fft.rfftfreq(frame_size, 1/SR)
        
        # Find peaks
        peaks = []
        for fi2 in range(1, len(mags)-1):
            if mags[fi2] > mags[fi2-1] and mags[fi2] > mags[fi2+1]:
                # Parabolic interpolation
                a, b, g = mags[fi2-1], mags[fi2], mags[fi2+1]
                if b > 0 and (a - 2*b + g) != 0:
                    p = 0.5 * (a - g) / (a - 2*b + g)
                    freq_interp = (fi2 + p) * SR / frame_size
                    amp_interp = b - 0.25*(a-g)*p
                    peaks.append((amp_interp, freq_interp, phases[fi2]))
        
        peaks.sort(key=lambda x: -x[0])
        
        frame_recon = np.zeros(frame_size)
        t_f = np.arange(frame_size) / SR
        for amp, freq, ph in peaks[:K_per_frame]:
            frame_recon += amp * 2/frame_size * np.cos(2*np.pi*freq*t_f + ph)
        
        recon_padded[start:start+frame_size] += frame_recon * window
        wsum[start:start+frame_size] += window**2
    
    mask = wsum > 1e-10
    recon_padded[mask] /= wsum[mask]
    return recon_padded[:n]

# 8. Gabor OMP
def gabor_omp(sig, K):
    n = len(sig); t_arr = np.arange(n) / SR
    vecs = []
    for t0 in [0.01,0.06,0.15,0.3,0.5]:
        for f0 in [130,196,262,440,700,1100,1760,2800,4400]:
            for s in [0.005,0.02,0.08,0.25]:
                v = np.exp(-((t_arr-t0)**2)/(2*s*s))*np.cos(2*np.pi*f0*(t_arr-t0))
                nm=np.linalg.norm(v)
                if nm>1e-10: v/=nm
                vecs.append(v)
    V = np.array(vecs); G = V @ V.T; d = V @ sig
    sel=[]; c=np.zeros(V.shape[0])
    for _ in range(min(K,V.shape[0])):
        rd=d-G[:,sel]@c[sel] if sel else d.copy()
        for s in sel: rd[s]=0
        b=int(np.argmax(np.abs(rd)))
        if abs(rd[b])<1e-10: break
        sel.append(b); sa=np.array(sel)
        try: cs=np.linalg.solve(G[np.ix_(sa,sa)],d[sa])
        except: cs=np.linalg.lstsq(G[np.ix_(sa,sa)],d[sa],rcond=None)[0]
        c[sa]=cs
    return V[sa].T@c[sa] if sel else np.zeros(n)

def main():
    piano = read_wav('/tmp/piano_c4.wav')[:N]
    guitar = read_wav('/tmp/guitar_c4.wav')[:N]
    def norm(s):
        mx = np.max(np.abs(s))
        return s*0.9/mx if mx>0 else s

    signals = {'piano': norm(piano), 'guitar': norm(guitar)}
    strategies = {
        'FFT':           global_fft,
        'STFT-256':      lambda s,K: stft_recon(s, K, 256),
        'STFT-512':      lambda s,K: stft_recon(s, K, 512),
        'STFT-1024':     lambda s,K: stft_recon(s, K, 1024),
        'STFT-4096':     lambda s,K: stft_recon(s, K, 4096),
        'MultiRes':      multires_stft,
        'FFT+Gabor':     fft_gabor_hybrid,
        'FFT+STFT':      fft_stft_hybrid,
        'FreqBand':      freq_band_split,
        'Sinusoidal':    sinusoidal_model,
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
