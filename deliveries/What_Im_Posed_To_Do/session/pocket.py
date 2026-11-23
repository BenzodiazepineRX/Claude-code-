"""Vocal-triggered dynamic bell cut on the beat's MID channel (sides untouched), zero-phase."""
import argparse, numpy as np, soundfile as sf
from scipy.signal import butter, sosfiltfilt, iirpeak
p=argparse.ArgumentParser(); p.add_argument('beat'); p.add_argument('vocal'); p.add_argument('out')
p.add_argument('--freq',type=float,default=2800); p.add_argument('--q',type=float,default=0.9)
p.add_argument('--depth',type=float,default=2.5); p.add_argument('--attack',type=float,default=0.02); p.add_argument('--release',type=float,default=0.25)
a=p.parse_args()
x,sr=sf.read(a.beat,always_2d=True); v,_=sf.read(a.vocal,always_2d=True)
L=len(x); v=np.pad(v,((0,max(0,L-len(v))),(0,0)))[:L]
M=(x[:,0]+x[:,1])/2; S=(x[:,0]-x[:,1])/2
# 2nd-order bandpass (unity peak) via RBJ
w0=2*np.pi*a.freq/sr; al=np.sin(w0)/(2*a.q)
b=np.array([al,0,-al]); aa=np.array([1+al,-2*np.cos(w0),1-al]); b/=aa[0]; aa/=aa[0]
from scipy.signal import tf2sos
bp=sosfiltfilt(tf2sos(b,aa),M)
# vocal envelope (dB), smoothed attack/release
vm=np.abs(v.mean(1)); hop=int(sr*0.005); n=L//hop
e=np.sqrt(np.convolve(vm**2,np.ones(hop*6)/(hop*6),mode='same')[::hop][:n]+1e-12)
ed=20*np.log10(e); thr=np.percentile(ed[ed>-80],95)-20
k=np.clip((ed-thr)/10,0,1)  # 0 below thr, full depth 10 dB above
env=np.zeros(n); ca=np.exp(-0.005/a.attack); cr=np.exp(-0.005/a.release)
for i in range(1,n):
    c=ca if k[i]>env[i-1] else cr; env[i]=c*env[i-1]+(1-c)*k[i]
envs=np.interp(np.arange(L),np.arange(n)*hop,env)
cut=1-10**(-a.depth*envs/20)
M2=M-cut*bp
y=np.stack([M2+S,M2-S],1)
sf.write(a.out,y.astype(np.float32),sr,subtype='FLOAT')
print(f'pocket: {a.freq:.0f} Hz Q{a.q} up to -{a.depth} dB on mid while vocal sings; engaged >50% depth {np.mean(envs>0.5)*100:.0f}% of song, mean cut {np.mean(a.depth*envs[envs>0.05]):.2f} dB when active')
