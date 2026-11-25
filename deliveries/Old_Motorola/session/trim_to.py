import sys, numpy as np, soundfile as sf
x,sr=sf.read(sys.argv[1],always_2d=True); ref=sf.info(sys.argv[3]).frames
y=np.zeros((ref,2),np.float32); n=min(ref,len(x)); y[:n]=x[:n]; f=int(0.4*sr); y[-f:]*=(np.linspace(1,0,f)[:,None]**2)
sf.write(sys.argv[2],y,sr,subtype='FLOAT')
