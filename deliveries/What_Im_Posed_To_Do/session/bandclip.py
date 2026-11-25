"""Two-band transient clip: zero-phase split at --split Hz (low + high = original exactly), 4x-oversampled tanh soft clip per band."""
import argparse, numpy as np, soundfile as sf
from scipy.signal import butter, sosfiltfilt, resample_poly
p=argparse.ArgumentParser(); p.add_argument('inp'); p.add_argument('out'); p.add_argument('--split',type=float,default=250)
p.add_argument('--low-reduce',type=float,default=2); p.add_argument('--high-reduce',type=float,default=5); p.add_argument('--knee',type=float,default=2)
a=p.parse_args(); x,sr=sf.read(a.inp,always_2d=True)
lo=sosfiltfilt(butter(4,a.split,'low',fs=sr,output='sos'),x,axis=0); hi=x-lo
def clip(s,red):
    if red<=0: return s, 0.0, 0.0
    pk=np.abs(s).max(); c=pk*10**(-red/20); k=c*10**(-a.knee/20); u=resample_poly(s,4,1,axis=0); sg=np.sign(u); m=np.abs(u); o=m>k
    m[o]=k+(c-k)*np.tanh((m[o]-k)/(c-k)); y=resample_poly(sg*m,1,4,axis=0)[:len(s)]
    return y, o.mean()*100, 20*np.log10(np.sqrt((s**2).mean()/(y**2).mean()))
l2,tl,rl=clip(lo,a.low_reduce); h2,th,rh=clip(hi,a.high_reduce); y=l2+h2
sf.write(a.out,y.astype(np.float32),sr,subtype='FLOAT')
print(f'bandclip: <{a.split:.0f} Hz -{a.low_reduce} dB (touched {tl:.2f}%, rms {rl:+.2f} dB) | >{a.split:.0f} Hz -{a.high_reduce} dB (touched {th:.2f}%, rms {rh:+.2f} dB) | peak {20*np.log10(abs(x).max()):.1f} -> {20*np.log10(abs(y).max()):.1f} dBFS, crest {20*np.log10(abs(x).max()/np.sqrt((x**2).mean())):.1f} -> {20*np.log10(abs(y).max()/np.sqrt((y**2).mean())):.1f} dB')
