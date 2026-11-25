import sys, numpy as np, soundfile as sf, pyloudnorm as pyln
for f in sys.argv[1:]:
    x,sr=sf.read(f,always_2d=True); m=pyln.Meter(sr); st=lambda a,b: m.integrated_loudness(x[int(a*sr):int(b*sr)])
    v=[st(20,40),st(70,100),st(125,140)]; h=[st(45,60),st(140,160)]
    print(f'{f:18s} verses {np.round(v,1)} | hooks {np.round(h,1)} | lift {np.mean(h)-np.mean(v):+.1f} LU')
