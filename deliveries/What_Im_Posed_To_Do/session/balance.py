"""Short-term loudness (approx, K-weighted via pyloudnorm) of each vocal vs beat in windows where that vocal is active."""
import sys, numpy as np, soundfile as sf, pyloudnorm as pyln
beat,sr=sf.read(sys.argv[1],always_2d=True); meter=pyln.Meter(sr)
def st(x,t): s=x[int(t*sr):int((t+3)*sr)]; return meter.integrated_loudness(s) if len(s)==3*sr else -99
for f in sys.argv[2:]:
    path,g=f.split(':'); v,_=sf.read(path,always_2d=True); v=v*10**(float(g)/20)
    d=[];
    for t in np.arange(20,158,3):
        lv=st(v,t)
        if lv>-35: d.append(lv-st(beat,t))
    d=np.array(d); print(f'{path:28s} gain {g:>5}: vocal-minus-beat short-term {np.median(d):+.1f} LU (n={len(d)}, IQR {np.percentile(d,25):+.1f}..{np.percentile(d,75):+.1f})')
