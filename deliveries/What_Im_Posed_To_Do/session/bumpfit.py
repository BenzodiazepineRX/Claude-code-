"""Fine bump measurement: level at 1/12-octave steps minus a 1-octave neighbourhood (active singing, both leads summed)."""
import sys, numpy as np, soundfile as sf
sr=44100
xs=[sf.read(f,always_2d=True)[0] for f in sys.argv[1].split(',')]; n=min(len(x) for x in xs); x=sum(v[:n] for v in xs); m=x.mean(1)
h=int(sr*0.05); k=len(m)//h; e=10*np.log10((m[:k*h].reshape(k,h)**2).mean(1)+1e-12); a=np.repeat(e>np.percentile(e[e>-80],95)-20,h); s=m[:k*h][a]
N=32768; P=0
for i in range(0,len(s)-N,N//2): P=P+np.abs(np.fft.rfft(s[i:i+N]*np.hanning(N)))**2
f=np.fft.rfftfreq(N,1/sr); d=10*np.log10(P+1e-20); lv=lambda fc,w: 10*np.log10(np.mean(10**(d[(f>fc/2**(w/2))&(f<fc*2**(w/2))]/10)))
fcs=[300*2**(i/12) for i in range(0,30)]; ex=[lv(fc,1/12)-lv(fc,1) for fc in fcs]
for fc,v in zip(fcs,ex):
    if 380<fc<720: print(f'{fc:6.0f} Hz {v:+5.1f} '+('#'*int(max(v,0)*5)))
