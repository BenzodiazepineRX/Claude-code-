"""5 ms fades at every region edge (region = audio between >=50 ms digital-silence runs)."""
import sys, numpy as np, soundfile as sf
x,sr=sf.read(sys.argv[1],always_2d=True); m=np.abs(x).max(1); z=m<1e-6; f=int(0.005*sr)
r=np.diff(np.concatenate([[0],z.astype(int),[0]])); st=np.where(r==1)[0]; en=np.where(r==-1)[0]; long_=(en-st)>int(0.05*sr)
g=np.ones(len(x)); n=0
for s,e in zip(st[long_],en[long_]):
    if e<len(x): g[e:e+f]=np.minimum(g[e:e+f],np.linspace(0,1,len(g[e:e+f]))); n+=1
    if s>0: a=max(0,s-f); g[a:s]=np.minimum(g[a:s],np.linspace(1,0,s-a)); n+=1
sf.write(sys.argv[2],(x*g[:,None]).astype(np.float32),sr,subtype='FLOAT'); print(f'edgefade: {n} edges faded (5 ms)')
