"""Pitch-independent harmonic envelope (300-800 Hz) vs 1-octave trend. usage: harmenv.py a.wav,b.wav"""
import sys, numpy as np, soundfile as sf
sr=44100; xs=[sf.read(f,always_2d=True)[0] for f in sys.argv[1].split(',')]; n=min(len(x) for x in xs); m=sum(v[:n] for v in xs).mean(1)
N=4096; fr=np.fft.rfftfreq(N,1/sr); w=np.hanning(N); pf=[]; pa=[]
for i in range(0,len(m)-N,2048):
    x=m[i:i+N]; r=np.sqrt((x**2).mean())
    if r<10**(-35/20): continue
    c=np.fft.irfft(np.abs(np.fft.rfft(x*w,2*N))**2)[:N]; lo,hi=int(sr/260),int(sr/80); L=lo+np.argmax(c[lo:hi])
    if c[L]/c[0]<0.6: continue
    f0=sr/L; S=np.abs(np.fft.rfft(x*w)); db=20*np.log10(S+1e-12)-20*np.log10(r)
    for k in range(1,20):
        if k*f0>900: break
        j=np.argmin(np.abs(fr-k*f0)); jj=slice(max(j-2,0),j+3); pf.append(fr[jj][np.argmax(S[jj])]); pa.append(db[jj].max())
pf=np.array(pf); pa=np.array(pa); bins=np.arange(300,820,20)
env=np.array([np.median(pa[(pf>=b-10)&(pf<b+10)]) if ((pf>=b-10)&(pf<b+10)).sum()>30 else np.nan for b in bins])
tr=np.array([np.nanmean(env[(bins>=b/2**0.5)&(bins<=b*2**0.5)]) for b in bins]); d=env-tr
sel=(bins>=440)&(bins<=520); print(f'hump 440-520 Hz: peak {np.nanmax(d[sel]):+.1f} dB, mean {np.nanmean(d[sel]):+.1f} dB | dip 580-620 Hz mean {np.nanmean(d[(bins>=580)&(bins<=620)]):+.1f} dB')
