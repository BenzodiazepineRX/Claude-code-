"""Gain-stage mix bus to -6 dBFS peak, then 2:1 glue (attack 20 / release 150 ms), threshold searched for ~1.5 dB avg GR on loud passages."""
import sys, subprocess, numpy as np, soundfile as sf
x,sr=sf.read(sys.argv[1],always_2d=True); g=10**(-6/20)/np.abs(x).max(); x=x*g
tmp=sys.argv[2]+'.pre.wav'; sf.write(tmp,x.astype(np.float32),sr,subtype='FLOAT')
def run(th,out):
    subprocess.run(['ffmpeg','-v','error','-y','-i',tmp,'-af',f'acompressor=threshold={th}dB:ratio=2:attack=20:release=150:knee=4:makeup=1','-c:a','pcm_f32le',out],check=True)
    y,_=sf.read(out,always_2d=True); n=min(len(x),len(y)); h=int(sr*0.4); m=n//h
    ex=10*np.log10((x[:m*h].reshape(m,h,2)**2).mean((1,2))+1e-12); ey=10*np.log10((y[:m*h].reshape(m,h,2)**2).mean((1,2))+1e-12)
    loud=ex>np.percentile(ex,60); return float(np.mean((ex-ey)[loud])), float(np.percentile((ex-ey)[loud],95))
for th in [-14,-16,-18,-20,-22,-24]:
    gr,p95=run(th,sys.argv[2])
    if gr>=1.3: break
print(f'glue: bus scaled {20*np.log10(g):+.1f} dB to -6 dBFS peak; 2:1 thr {th} dB -> avg GR {gr:.1f} dB on loud passages (95th pct {p95:.1f} dB)')
