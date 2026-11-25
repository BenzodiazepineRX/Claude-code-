import sys, numpy as np, soundfile as sf
x,sr=sf.read(sys.argv[1],always_2d=True); m=x.mean(1); hop=int(sr*0.01)
n=len(m)//hop; e=10*np.log10(np.convolve(m**2,np.ones(hop*3)/(hop*3),'same')[::hop][:n]+1e-12)
act=e>np.percentile(e[e>-80],95)-22
rng=[]; secs=[(40,60),(140,160)]
for i in range(1,n-40):
    t=i*0.01
    if act[i-1] and not act[i:i+40].any() and act[max(0,i-30):i].mean()>0.7 and any(a<=t<=b for a,b in secs):
        rng.append(f'{t-0.35:.2f}-{t:.2f}')
print(','.join(rng))
