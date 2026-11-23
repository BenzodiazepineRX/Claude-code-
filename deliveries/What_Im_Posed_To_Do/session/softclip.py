"""4x-oversampled tanh soft clipper: shaves the top --reduce dB of peaks (knee starts --knee dB below the new ceiling)."""
import argparse, numpy as np, soundfile as sf
from scipy.signal import resample_poly
p=argparse.ArgumentParser(); p.add_argument('inp'); p.add_argument('out'); p.add_argument('--reduce',type=float,default=1.5); p.add_argument('--knee',type=float,default=2.0)
a=p.parse_args(); x,sr=sf.read(a.inp,always_2d=True); pk=np.abs(x).max()
c=pk*10**(-a.reduce/20); k=c*10**(-a.knee/20)
u=resample_poly(x,4,1,axis=0); s=np.sign(u); m=np.abs(u)
over=m>k; m[over]=k+(c-k)*np.tanh((m[over]-k)/(c-k)); y=resample_poly(s*m,1,4,axis=0)[:len(x)]
sf.write(a.out,y.astype(np.float32),sr,subtype='FLOAT')
print(f'softclip: knee {20*np.log10(k/pk):.1f} dB, ceiling {20*np.log10(c/pk):.1f} dB re: peak; samples touched {over.mean()*100:.2f}%, RMS change {20*np.log10(np.sqrt((x**2).mean()/(y**2).mean())):.2f} dB, peak {20*np.log10(pk):.1f} -> {20*np.log10(np.abs(y).max()):.1f} dBFS')
