"""Phrase/word volume rider: evens out short-term level of active vocal, +/- max dB, holds gain in gaps."""
import argparse, numpy as np, soundfile as sf
p=argparse.ArgumentParser(); p.add_argument('inp'); p.add_argument('out')
p.add_argument('--max-db',type=float,default=3.0); p.add_argument('--amount',type=float,default=0.7)
p.add_argument('--win',type=float,default=0.4); p.add_argument('--smooth',type=float,default=0.12)
a=p.parse_args()
x,sr=sf.read(a.inp,always_2d=True); m=x.mean(1)
hop=int(sr*0.01); w=int(sr*a.win); n=len(m)//hop
c=np.concatenate([[0],np.cumsum(m**2)]); idx=np.arange(n)*hop; lo=np.clip(idx-w//2,0,len(m)); hi=np.clip(idx+w//2,0,len(m)); p2=(c[hi]-c[lo])/np.maximum(hi-lo,1)
lev=10*np.log10(p2+1e-12)
act=lev>(np.percentile(lev[lev>-80],95)-18) if (lev>-80).any() else lev>-60
tgt=np.median(lev[act])
g=np.zeros(n); cur=0.0
for i in range(n):
    if act[i]: cur=np.clip((tgt-lev[i])*a.amount,-a.max_db,a.max_db)
    g[i]=cur
# smooth (one-pole forward+backward for no lag)
al=np.exp(-1/(a.smooth/0.01))
for arr in (g,):
    for i in range(1,n): arr[i]=al*arr[i-1]+(1-al)*arr[i]
    for i in range(n-2,-1,-1): arr[i]=al*arr[i+1]+(1-al)*arr[i]
gs=np.interp(np.arange(len(m)),np.arange(n)*hop,g)
y=x*(10**(gs/20))[:,None]
sf.write(a.out,y.astype(np.float32),sr,subtype='FLOAT')
sp=lambda v:np.std(v)
la=lev[act]; lb=(lev+g)[act]
print(f'rider: target {tgt:.1f} dB, active {act.mean()*100:.0f}% | gain range {g[act].min():+.1f}..{g[act].max():+.1f} dB, mean |g| {np.abs(g[act]).mean():.2f} dB')
print(f'rider: short-term level spread (std) {sp(la):.2f} -> {sp(lb):.2f} dB')
