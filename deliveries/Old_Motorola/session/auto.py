"""Section gain automation with smooth ramps: auto.py IN OUT 40-60:+1.5,140-160:+1.5 [--ramp 0.3]"""
import sys, numpy as np, soundfile as sf
x,sr=sf.read(sys.argv[1],always_2d=True); ramp=float(sys.argv[4]) if len(sys.argv)>4 else 0.3
g=np.zeros(len(x))
for s in sys.argv[3].split(','):
    r,d=s.split(':'); a,b=map(float,r.split('-')); g[int(a*sr):int(b*sr)]=float(d)
k=int(ramp*sr); gp=np.pad(g,(k,k),mode='edge'); c=np.concatenate([[0],np.cumsum(gp)]); g=((c[k:]-c[:-k])/k)[k//2:k//2+len(g)]
sf.write(sys.argv[2],(x*10**(g/20)[:,None]).astype(np.float32),sr,subtype='FLOAT'); print('auto',sys.argv[3])
