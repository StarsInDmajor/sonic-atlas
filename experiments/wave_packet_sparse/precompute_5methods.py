#!/usr/bin/env python3
"""
Precompute 5 sparse reconstruction methods.
Methods: FFT Top-K, DCT Top-K, MP+Gabor, OMP+Gabor, BP/ISTA.
Run with: nix-shell -p python3Packages.numpy python3Packages.scipy --run "python3 precompute_5methods.py"
"""
import json, cmath, struct, wave, sys, math
import numpy as np

SR = 44100; DUR = 0.6; N = int(DUR * SR)  # 26460
DS = max(1, N // 400)  # 66
NP = N // DS            # 400
BKPTS = [1,2,3,5,8,10,15,20,30,50,80,120,200]

# Gabor dictionary
T0S    = [0.01, 0.06, 0.15, 0.3, 0.5]
F0S    = [130, 196, 262, 440, 700, 1100, 1760, 2800, 4400]
SIGMAS = [0.005, 0.02, 0.08, 0.25]

def read_wav(path):
    w = wave.open(path, 'r')
    nch, sw, sr, nf = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
    raw = w.readframes(nf); w.close()
    if sw == 2:
        s = np.frombuffer(raw, dtype=np.int16).reshape(-1, nch).mean(axis=1).astype(np.float64)/32768.0
    elif sw == 4:
        s = np.frombuffer(raw, dtype=np.int32).reshape(-1, nch).mean(axis=1).astype(np.float64)/2147483648.0
    else:
        raise ValueError(f"Unsupported: {sw}")
    return s[:N]

def build_dictionary():
    t_arr = np.arange(N, dtype=np.float64) / SR
    atoms = []; vecs = []
    for t0 in T0S:
        for f0 in F0S:
            for sigma in SIGMAS:
                v = np.exp(-((t_arr-t0)**2)/(2*sigma**2)) * np.cos(2*np.pi*f0*(t_arr-t0))
                nm = np.linalg.norm(v)
                if nm > 1e-10: v /= nm
                atoms.append((t0, f0, sigma))
                vecs.append(v)
    return atoms, np.array(vecs)  # (n_atoms, N)

def run_mp(sig, V, n_iter=30):
    """Matching Pursuit (greedy, non-orthogonal)."""
    N = len(sig); n_atoms = V.shape[0]
    residual = sig.copy(); sigE = np.dot(sig, sig)
    selected = []
    for step in range(n_iter):
        scores = np.abs(V @ residual)
        scores[[s[0] for s in selected]] = 0
        best = int(np.argmax(scores))
        if scores[best] < 1e-10: break
        c = np.dot(V[best], residual)
        residual -= c * V[best]
        selected.append((best, float(c)))
        if (step+1) % 10 == 0:
            print(f"    MP {step+1}: resid={np.dot(residual,residual)/sigE*100:.1f}%", file=sys.stderr)
    return selected

def run_omp(sig, V, n_iter=30):
    """OMP with Gram matrix."""
    n_atoms = V.shape[0]; sigE = np.dot(sig, sig)
    print(f"    Gram ({n_atoms}x{n_atoms})...", file=sys.stderr)
    G = V @ V.T  # (n_atoms, n_atoms)
    d = V @ sig   # (n_atoms,)
    selected = []; coefs = np.zeros(n_atoms)
    for step in range(n_iter):
        sel_set = set(selected)
        res_dots = d - G[:, selected] @ coefs[selected] if selected else d.copy()
        res_dots[list(sel_set)] = 0
        best = int(np.argmax(np.abs(res_dots)))
        if abs(res_dots[best]) < 1e-10: break
        selected.append(best)
        sel = np.array(selected)
        Gss = G[np.ix_(sel, sel)]
        ds = d[sel]
        try: cs = np.linalg.solve(Gss, ds)
        except: cs = np.linalg.lstsq(Gss, ds, rcond=None)[0]
        coefs[sel] = cs
        if (step+1) % 5 == 0:
            recon = V[sel].T @ coefs[sel]
            r = np.dot(sig-recon, sig-recon)/sigE
            print(f"    OMP {step+1}: resid={r*100:.1f}%", file=sys.stderr)
    return [(idx, float(coefs[idx])) for idx in selected]

def run_bp_ista(sig, V, max_iter=500):
    """Basis Pursuit via ISTA (ℓ₁ minimization)."""
    n_atoms = V.shape[0]; sigE = np.dot(sig, sig)
    c = np.zeros(n_atoms)
    lam = 0.005 * np.max(np.abs(sig))
    # Estimate step size via power iteration on Hessian V @ V.T
    x = np.random.randn(n_atoms)
    for _ in range(10):
        x = V @ (V.T @ x)
        x /= np.linalg.norm(x)
    L = np.linalg.norm(V @ (V.T @ x)) / np.linalg.norm(x)
    step = 1.0 / (L * 1.1)
    
    for it in range(max_iter):
        residual = V @ (V.T @ c - sig)  # gradient: V @ (recon - sig)
        z = c - step * residual
        c = np.sign(z) * np.maximum(np.abs(z) - lam * step, 0)
        if (it+1) % 100 == 0:
            recon = V.T @ c
            r = np.dot(sig-recon, sig-recon)/sigE
            nnz = np.sum(np.abs(c) > 1e-8)
            print(f"    ISTA {it+1}: resid={r*100:.1f}%, nnz={nnz}", file=sys.stderr)
    idx = np.argsort(-np.abs(c))
    return [(int(i), float(c[i])) for i in idx if abs(c[i]) > 1e-8]

def compute_residuals(sig, fc_full, fftN, dct_c, mp_atoms, omp_atoms, bp_atoms, V):
    sigE = np.dot(sig, sig)
    Nsig = len(sig)
    mags = np.abs(fc_full[:fftN//2])
    phases = np.angle(fc_full[:fftN//2])
    n_bins = len(mags)
    dct_mags = np.abs(dct_c)
    
    results = {'fft':[], 'dct':[], 'mp':[], 'omp':[], 'bp':[]}
    for K in BKPTS:
        print(f"    K={K}...", file=sys.stderr)
        
        # FFT Top-K
        top = np.argsort(mags)[::-1][:K]
        recon = np.zeros(Nsig)
        for idx in top:
            freq = idx * SR / fftN
            recon += mags[idx]/Nsig*2 * np.cos(2*np.pi*freq*np.arange(Nsig)/SR + phases[idx])
        r = float(np.dot(sig-recon, sig-recon)/sigE)
        results['fft'].append((K, round(min(r,1.0),6)))
        
        # DCT Top-K
        dct_top = np.argsort(dct_mags)[::-1][:K]
        recon_dct = np.zeros(Nsig)
        for idx in dct_top:
            c = dct_c[idx]
            scale = (1.0/Nsig) if idx==0 else (2.0/Nsig)
            recon_dct += c * scale * np.cos(np.pi/Nsig * (np.arange(Nsig)+0.5) * idx)
        r = float(np.dot(sig-recon_dct, sig-recon_dct)/sigE)
        results['dct'].append((K, round(min(r,1.0),6)))
        
        # MP Top-K
        if K <= len(mp_atoms):
            sel = [i for i,_ in mp_atoms[:K]]
            cs = np.array([c for _,c in mp_atoms[:K]])
            recon_mp = V[sel].T @ cs
            r = float(np.dot(sig-recon_mp, sig-recon_mp)/sigE)
            results['mp'].append((K, round(min(r,1.0),6)))
        
        # OMP Top-K (re-solve normal equations for each K subset)
        if K <= len(omp_atoms):
            sel = [i for i,_ in omp_atoms[:K]]
            Gss = V[sel] @ V[sel].T
            ds = V[sel] @ sig
            try: cs = np.linalg.solve(Gss, ds)
            except: cs = np.linalg.lstsq(Gss, ds, rcond=None)[0]
            recon_omp = V[sel].T @ cs
            r = float(np.dot(sig-recon_omp, sig-recon_omp)/sigE)
            results['omp'].append((K, round(min(r,1.0),6)))
        
        # BP Top-K
        if bp_atoms and K <= len(bp_atoms):
            sel = [i for i,_ in bp_atoms[:K]]
            cs = np.array([c for _,c in bp_atoms[:K]])
            recon_bp = V[sel].T @ cs
            r = float(np.dot(sig-recon_bp, sig-recon_bp)/sigE)
            results['bp'].append((K, round(min(r,1.0),6)))
    
    return results

def main():
    print("=== 5 methods (numpy) ===", file=sys.stderr)
    
    piano = read_wav('/tmp/piano_c4.wav')
    guitar = read_wav('/tmp/guitar_c4.wav')
    
    def norm(s):
        mx = np.max(np.abs(s))
        return s * 0.9 / mx if mx > 0 else s
    
    signals = {
        'piano': {'sig': norm(piano), 'label': '钢琴 C4 (262Hz)'},
        'guitar': {'sig': norm(guitar), 'label': '吉他 C4 (262Hz)'},
    }
    
    print("Building dictionary...", file=sys.stderr)
    atoms, V = build_dictionary()
    print(f"  {V.shape[0]} atoms × {V.shape[1]} pts", file=sys.stderr)
    
    results = {}
    for pk, info in signals.items():
        print(f"\n=== {pk} ===", file=sys.stderr)
        sig = info['sig']
        sigE = float(np.dot(sig, sig))
        
        # FFT
        fftN = 1
        while fftN < len(sig): fftN <<= 1
        padded = np.zeros(fftN); padded[:N] = sig
        fc = np.fft.fft(padded)
        mags = np.abs(fc[:fftN//2])/N*2
        mx = np.max(mags)
        top = np.argsort(mags)[::-1][:300]
        fft_bins = [{'k':int(i),'m':round(float(mags[i]),6),'p':round(float(np.angle(fc[i])),4)} 
                    for i in top if mags[i] > mx*0.001]
        fa = int(np.sum(mags > mx*0.01))
        
        # DCT
        dct_c = np.zeros(N)
        for k in range(N):
            dct_c[k] = np.sum(sig * np.cos(np.pi/N * (np.arange(N)+0.5) * k))
        dct_mags = np.abs(dct_c)
        fa_dct = int(np.sum(dct_mags > np.max(dct_mags)*0.01))
        
        # MP
        print("  MP (30)...", file=sys.stderr)
        mp_sel = run_mp(sig, V, 30)
        
        # OMP
        print("  OMP (30)...", file=sys.stderr)
        omp_sel = run_omp(sig, V, 30)
        
        # BP
        print("  BP/ISTA (500)...", file=sys.stderr)
        bp_sel = run_bp_ista(sig, V, 500)
        
        # Residuals
        print("  Residuals...", file=sys.stderr)
        resid = compute_residuals(sig, fc, fftN, dct_c, mp_sel, omp_sel, bp_sel, V)
        
        def atom_meta(sel):
            return [{'t0':atoms[i][0],'f0':atoms[i][1],'sigma':atoms[i][2],'amp':round(c,4)} for i,c in sel]
        
        sig_dsp = sig[::DS][:NP]
        results[pk] = {
            'label': info['label'],
            's4': [round(float(v),6) for v in sig_dsp],
            'fa': fa, 'fa_dct': fa_dct,
            'fb': fft_bins,
            'at': atom_meta(mp_sel),
            'at_omp': atom_meta(omp_sel),
            'at_bp': atom_meta(bp_sel[:30]),
            'resid': resid,
        }
        for m, vals in resid.items():
            if vals:
                d = dict(vals)
                print(f"  {m}: K=1={d.get(1,0)*100:.1f}% K=10={d.get(10,0)*100:.1f}% K=30={d.get(30,0)*100:.1f}%", file=sys.stderr)
    
    out = json.dumps(results, separators=(',', ':'))
    print(f"\nOutput: {len(out)} bytes", file=sys.stderr)
    print(out)

if __name__ == '__main__':
    main()
