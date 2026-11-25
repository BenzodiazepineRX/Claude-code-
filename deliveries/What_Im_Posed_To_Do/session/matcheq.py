"""Reference match EQ: per-1/3-octave tone difference (active singing only) between a REFERENCE vocal set and a TARGET vocal set,
smoothed and clamped, realised as a linear-phase FIR. usage: matcheq.py design REF1,REF2 TGT1,TGT2 curve.json | apply curve.json IN OUT"""
import sys, json, numpy as np, soundfile as sf
from scipy.signal import firwin2, fftconvolve
sr=44100; CEN=[250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300,8000,10000]
def third(files):
    tot=None
    for f in files:
        x,_=sf.read(f,always_2d=True); m=x.mean(1); h=int(sr*0.05); n=len(m)//h
        e=10*np.log10((m[:n*h].reshape(n,h)**2).mean(1)+1e-12); act=np.repeat(e>np.percentile(e[e>-80],95)-20,h); m=m[:n*h][act]
        N=8192; P=0
        for i in range(0,len(m)-N,N//2): P=P+np.abs(np.fft.rfft(m[i:i+N]*np.hanning(N)))**2
        tot=P if tot is None else tot+P
    fr=np.fft.rfftfreq(8192,1/sr); out=np.array([10*np.log10(tot[(fr>=c/2**(1/6))&(fr<c*2**(1/6))].sum()+1e-20) for c in CEN])
    return out-np.mean(out[6:9])   # normalise at 1-1.6 kHz
if sys.argv[1]=='design':
    r=third(sys.argv[2].split(',')); t=third(sys.argv[3].split(',')); d=r-t
    d=np.convolve(np.pad(d,1,mode='edge'),[0.25,0.5,0.25],'valid')      # smooth across neighbours
    d=np.clip(d,-4.0,4.5); d-=np.mean(d[6:9])                              # no overall level change around 1-1.6k
    json.dump({'cent':CEN,'gain_db':[round(float(v),2) for v in d]},open(sys.argv[4],'w'))
    for c,g in zip(CEN,d): print(f'{c:6d} Hz {g:+5.1f} dB '+('#'*int(abs(g)*4)))
else:
    cv=json.load(open(sys.argv[2])); c=np.array(cv['cent'],float); g=np.array(cv['gain_db'])
    f=np.concatenate([[0],[c[0]/2],c,[14000,sr/2]]); gg=np.concatenate([[g[0]],[g[0]],g,[g[-1]],[g[-1]]])
    taps=firwin2(4097,f/(sr/2),10**(gg/20)); x,_=sf.read(sys.argv[3],always_2d=True)
    y=np.stack([fftconvolve(x[:,ch],taps)[2048:2048+len(x)] for ch in range(x.shape[1])],1)
    sf.write(sys.argv[4],y.astype(np.float32),sr,subtype='FLOAT'); print('match EQ applied (linear phase, 4097 taps, latency compensated) ->',sys.argv[4])
