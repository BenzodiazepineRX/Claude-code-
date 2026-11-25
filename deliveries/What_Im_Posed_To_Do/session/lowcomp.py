"""Low-band (808) compressor: zero-phase split at --split Hz, compress only the low band (ffmpeg acompressor), recombine exactly."""
import argparse, subprocess, numpy as np, soundfile as sf
from scipy.signal import butter, sosfiltfilt
p=argparse.ArgumentParser(); p.add_argument('inp'); p.add_argument('out'); p.add_argument('--split',type=float,default=150)
p.add_argument('--thr',type=float,default=-18); p.add_argument('--ratio',type=float,default=3); p.add_argument('--attack',type=float,default=15); p.add_argument('--release',type=float,default=120)
a=p.parse_args(); x,sr=sf.read(a.inp,always_2d=True)
lo=sosfiltfilt(butter(4,a.split,'low',fs=sr,output='sos'),x,axis=0); hi=x-lo
sf.write(a.out+'.lo.wav',lo.astype(np.float32),sr,subtype='FLOAT')
subprocess.run(['ffmpeg','-v','error','-y','-i',a.out+'.lo.wav','-af',f'acompressor=threshold={a.thr}dB:ratio={a.ratio}:attack={a.attack}:release={a.release}:knee=4:detection=rms:makeup=1','-c:a','pcm_f32le',a.out+'.loc.wav'],check=True)
lc,_=sf.read(a.out+'.loc.wav',always_2d=True); lc=lc[:len(lo)]
h=int(sr*0.05); n=len(lo)//h; e1=10*np.log10((lo[:n*h].reshape(n,h,2)**2).mean((1,2))+1e-12); e2=10*np.log10((lc[:n*h].reshape(n,h,2)**2).mean((1,2))+1e-12)
act=e1>np.percentile(e1,90)-15; gr=(e1-e2)[act]
y=lc+hi; sf.write(a.out,y.astype(np.float32),sr,subtype='FLOAT')
print(f'lowcomp <{a.split:.0f} Hz thr {a.thr} {a.ratio}:1 {a.attack}/{a.release} ms: avg GR {gr.mean():.1f} dB (95th {np.percentile(gr,95):.1f}); 808 note-to-note spread {np.std(e1[act]):.1f} -> {np.std(e2[act]):.1f} dB')
