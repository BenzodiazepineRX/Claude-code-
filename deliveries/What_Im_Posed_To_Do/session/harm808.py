"""808 audibility on a phone: per 186 ms frame, detect the 808 note (strongest 40-120 Hz peak); in the phone-simulated signal
(mono, 300-7000 Hz) measure energy within +/-2.5% of that note's harmonics (300-1200 Hz) vs total phone-band energy. Reported in dB (higher = more audible)."""
import sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfiltfilt
sr=44100
def h808(f,secs=((31,58),(66,87),(116,143),(158,173))):
    x,_=sf.read(f,always_2d=True); m=x.mean(1); ph=sosfiltfilt(butter(4,[300,7000],'band',fs=sr,output='sos'),m)
    N=8192; fr=np.fft.rfftfreq(N,1/sr); out=[]
    for a,b in secs:
        for i in range(int(a*sr),int(b*sr)-N,N):
            S=np.abs(np.fft.rfft(m[i:i+N]*np.hanning(N)))**2; lo=(fr>40)&(fr<120)
            if S[lo].sum()<1e-6*S.sum(): continue
            f0=fr[lo][np.argmax(S[lo])]; P=np.abs(np.fft.rfft(ph[i:i+N]*np.hanning(N)))**2
            mask=np.zeros_like(fr,bool)
            for k in range(2,40):
                hk=k*f0
                if 300<=hk<=1200: mask|=(fr>hk*0.975)&(fr<hk*1.025)
            out.append(10*np.log10(P[mask].sum()/P[(fr>300)&(fr<7000)].sum()+1e-12))
    return np.median(out)
for f in sys.argv[1:]: print(f'{f:40s} 808 harmonics share of phone band: {h808(f):6.1f} dB')
