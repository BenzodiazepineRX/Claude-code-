"""808 harmonic enhancer: isolate <120 Hz, saturate (4x oversampled), keep only the new harmonics 150-900 Hz, blend into the MID channel."""
import argparse, numpy as np, soundfile as sf
from scipy.signal import butter, sosfiltfilt, resample_poly
p=argparse.ArgumentParser(); p.add_argument('inp'); p.add_argument('out'); p.add_argument('--level',type=float,default=-12); p.add_argument('--drive',type=float,default=12)
a=p.parse_args(); x,sr=sf.read(a.inp,always_2d=True); M=(x[:,0]+x[:,1])/2; S=(x[:,0]-x[:,1])/2
sub=sosfiltfilt(butter(4,120,'low',fs=sr,output='sos'),M); pk=np.abs(sub).max()
u=resample_poly(sub/pk,4,1)*10**(a.drive/20); h=np.tanh(u+0.2)-np.tanh(0.2); h=resample_poly(h,1,4)[:len(M)]
h=sosfiltfilt(butter(4,[150,900],'band',fs=sr,output='sos'),h); h*=pk/ (np.sqrt((h**2).mean())+1e-12) * np.sqrt((sub**2).mean())/pk * 10**(a.level/20)
M2=M+h; y=np.stack([M2+S,M2-S],1); sf.write(a.out,y.astype(np.float32),sr,subtype='FLOAT')
print(f'808 enhancer: harmonics 150-900 Hz at {a.level} dB re: sub RMS, drive {a.drive} dB; full-mix RMS change {10*np.log10((y**2).mean()/(x**2).mean()):+.2f} dB')
