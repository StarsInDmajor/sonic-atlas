#!/usr/bin/env python3
"""
Final precompute: 4 working strategies for §4 demo.
Run: nix-shell -p python3Packages.numpy --run "python3 precompute_final.py"
Output: JSON with residual curves for each method × each signal.
"""
import numpy as np
import wave, sys, json

SR = 44100; DUR = 0.6; N = int(DUR * SR); DS = 66; NP = 400
BKPTS = [1, 2, 3, 5, 8, 10, 15, 20, 30, 50, 80, 120, 200]

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
# Strategy 1: Global FFT top-K
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
# Strategy 2: FFT tonal + Gabor OMP residual
# ============================================================================
def fft_gabor_hybrid(sig, K):
    n = len(sig)
    K_fft = max(1, int(K * 0.7))
    K_gabor = max(1, K - K_fft)
    recon_fft = global_fft(sig, K_fft)
    residual = sig - recon_fft
    
    t_arr = np.arange(n) / SR
    vecs = []
    for t0 in [0.01, 0.06, 0.15, 0.3, 0.5]:
        for f0 in [130, 196, 262, 440, 700, 1100, 1760, 2800, 4400]:
            for sigma in [0.005, 0.02, 0.08, 0.25]:
                v = np.exp(-((t_arr-t0)**2)/(2*sigma**2)) * np.cos(2*np.pi*f0*(t_arr-t0))
                nm = np.linalg.norm(v)
                if nm > 1e-10: v /= nm
                vecs.append(v)
    V = np.array(vecs)
    G = V @ V.T; d = V @ residual
    sel = []; c = np.zeros(V.shape[0])
    for _ in range(min(K_gabor, V.shape[0])):
        rd = d - G[:, sel] @ c[sel] if sel else d.copy()
        for s in sel: rd[s] = 0
        best = int(np.argmax(np.abs(rd)))
        if abs(rd[best]) < 1e-10: break
        sel.append(best)
        sa = np.array(sel)
        try: cs = np.linalg.solve(G[np.ix_(sa, sa)], d[sa])
        except: cs = np.linalg.lstsq(G[np.ix_(sa, sa)], d[sa], rcond=None)[0]
        c[sa] = cs
    recon_gabor = V[sa].T @ c[sa] if sel else np.zeros(n)
    return recon_fft + recon_gabor

# ============================================================================
# Strategy 3: Frequency band splitting
# ============================================================================
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

# ============================================================================
# Strategy 4: Gabor OMP (reference baseline)
# ============================================================================
def gabor_omp(sig, K):
    n = len(sig); t_arr = np.arange(n) / SR
    vecs = []
    for t0 in [0.01, 0.06, 0.15, 0.3, 0.5]:
        for f0 in [130, 196, 262, 440, 700, 1100, 1760, 2800, 4400]:
            for sigma in [0.005, 0.02, 0.08, 0.25]:
                v = np.exp(-((t_arr-t0)**2)/(2*sigma**2)) * np.cos(2*np.pi*f0*(t_arr-t0))
                nm = np.linalg.norm(v)
                if nm > 1e-10: v /= nm
                vecs.append(v)
    V = np.array(vecs); G = V @ V.T; d = V @ sig
    sel = []; c = np.zeros(V.shape[0])
    for _ in range(min(K, V.shape[0])):
        rd = d - G[:, sel] @ c[sel] if sel else d.copy()
        for s in sel: rd[s] = 0
        best = int(np.argmax(np.abs(rd)))
        if abs(rd[best]) < 1e-10: break
        sel.append(best)
        sa = np.array(sel)
        try: cs = np.linalg.solve(G[np.ix_(sa, sa)], d[sa])
        except: cs = np.linalg.lstsq(G[np.ix_(sa, sa)], d[sa], rcond=None)[0]
        c[sa] = cs
    return V[sa].T @ c[sa] if sel else np.zeros(n)

# ============================================================================
# Main
# ============================================================================
def main():
    piano = read_wav('/tmp/piano_c4.wav')[:N]
    guitar = read_wav('/tmp/guitar_c4.wav')[:N]
    def norm(s):
        mx = np.max(np.abs(s))
        return s*0.9/mx if mx>0 else s

    signals = {
        'piano': {'sig': norm(piano), 'label': '钢琴 C4 (262Hz)'},
        'guitar': {'sig': norm(guitar), 'label': '吉他 C4 (262Hz)'},
    }

    strategies = {
        'fft': ('FFT Top-K', global_fft),
        'hybrid': ('FFT+Gabor', fft_gabor_hybrid),
        'freqband': ('FreqBand', freq_band_split),
        'gabor': ('Gabor OMP', gabor_omp),
    }

    results = {}
    for sn, info in signals.items():
        sig = info['sig']
        print(f"\n=== {sn} ===", file=sys.stderr)

        # FFT metadata (for spectrum display)
        fftN = 1
        while fftN < N: fftN <<= 1
        fc = np.fft.rfft(sig, n=fftN)
        mags_full = np.abs(fc)
        mx_mag = np.max(mags_full)
        top_fft = np.argsort(mags_full)[::-1][:300]
        fb = []
        for idx in top_fft:
            if mags_full[idx] < mx_mag * 0.001: break
            fb.append({
                'k': int(idx),
                'm': round(float(mags_full[idx]), 6),
                'p': round(float(np.angle(fc[idx])), 4)
            })
        fa = int(np.sum(mags_full > mx_mag * 0.01))

        # Display signal
        sig_disp = sig[::DS][:NP]

        # Compute residuals for all strategies
        resid_data = {}
        for key, (name, fn) in strategies.items():
            print(f"  {name}:", file=sys.stderr, end='')
            vals = []
            for K in BKPTS:
                try:
                    recon = fn(sig, K)
                    r = resid(sig, recon)
                    vals.append((K, round(r, 6)))
                    print(f" {K}→{r*100:.1f}%", file=sys.stderr, end='')
                except Exception as e:
                    vals.append((K, None))
                    print(f" {K}→ERR", file=sys.stderr, end='')
            resid_data[key] = vals
            print(file=sys.stderr)

        results[sn] = {
            'label': info['label'],
            's4': [round(float(v), 6) for v in sig_disp],
            'fa': fa,
            'fb': fb,
            'resid': resid_data,
        }

    out = json.dumps(results, separators=(',', ':'))
    print(f"\nOutput: {len(out)} bytes", file=sys.stderr)
    print(out)

if __name__ == '__main__':
    main()
