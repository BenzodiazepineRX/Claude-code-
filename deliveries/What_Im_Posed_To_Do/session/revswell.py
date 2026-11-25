"""Reverse-reverb swells: reverse the reverb tail of each entry word so it swells INTO the entry. usage: revswell.py WET OUT t1,t2 [len_s]"""
import sys, numpy as np, soundfile as sf
w,sr=sf.read(sys.argv[1],always_2d=True); ts=[float(t) for t in sys.argv[3].split(',')]; ln=float(sys.argv[4]) if len(sys.argv)>4 else 2.5
out=np.zeros_like(w); n=int(ln*sr); f=int(0.03*sr)
for t in ts:
    i=int(t*sr); tail=w[i:i+n][::-1].copy(); tail[-f:]*=np.linspace(1,0,f)[:,None]; tail[:f]*=np.linspace(0,1,f)[:,None]; out[i-n:i]+=tail
sf.write(sys.argv[2],out.astype(np.float32),sr,subtype='FLOAT'); print('reverse swells into',ts)
