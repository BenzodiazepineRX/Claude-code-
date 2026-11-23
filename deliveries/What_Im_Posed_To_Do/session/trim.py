import sys, numpy as np, soundfile as sf
x,sr=sf.read(sys.argv[1],always_2d=True); a=np.abs(x).max(1)
last=np.where(a>10**(-70/20))[0][-1]; end=min(len(x),last+int(0.4*sr)); y=x[:end].copy()
f=int(0.4*sr); y[-f:]*=np.linspace(1,0,f)[:,None]**2
sf.write(sys.argv[2],y.astype(np.float32),sr,subtype='FLOAT'); print(f'trim: last audio (>-70 dBFS) at {last/sr:.2f}s, new length {end/sr:.2f}s (was {len(x)/sr:.2f}s), 0.4 s fade')
