"""Align copy-pasted hook-2 regions to their hook-1 originals (32 bars earlier). Regions = audio between >=50 ms digital silence in the SOURCE stem.
Only regions that are clear copies (corr >= 0.9) are moved; others (fresh takes) are left as performed. usage: regionalign.py SRC PROCESSED_IN OUT"""
import sys, numpy as np, soundfile as sf
src,sr=sf.read(sys.argv[1],always_2d=True); pin,_=sf.read(sys.argv[2],always_2d=True); s=src.mean(1); L=int(round(32*4*60/135*sr))
z=np.abs(s)<1e-6; r=np.diff(np.concatenate([[0],z.astype(int),[0]])); st=np.where(r==1)[0]; en=np.where(r==-1)[0]; lg=(en-st)>int(0.05*sr)
starts=en[lg]; ends=st[lg]; regs=[(a,b) for a,b in zip(np.concatenate([[0],starts]),np.concatenate([ends,[len(s)]])) if b-a>int(0.05*sr) and np.abs(s[a:b]).max()>1e-4]
out=pin.copy(); log=[]
for a,b in regs:
    if not (98.5*sr<=a<=129*sr): continue
    seg=s[a:b]; best=(-1,0)
    for d in range(-int(0.06*sr),int(0.06*sr)):
        i=a-L+d
        if i<0: continue
        B=s[i:i+len(seg)]; c=np.dot(seg,B)/(np.linalg.norm(seg)*np.linalg.norm(B)+1e-12)
        if c>best[0]: best=(c,d)
    c,d=best; shift=-d  # region sits d samples later than (orig+32 bars)? d<0 means orig is earlier
    # orig position = a-L+d  -> region should move to orig+L = a+d
    if c>=0.9 and d!=0:
        piece=pin[a:b].copy(); out[a:b]=0; out[a+d:b+d]+=piece; log.append(f'{a/sr:7.2f}-{b/sr:7.2f}s copy (corr {c:.3f}) moved {d/sr*1000:+.1f} ms')
    else: log.append(f'{a/sr:7.2f}-{b/sr:7.2f}s {"fresh take" if c<0.9 else "already aligned"} (corr {c:.3f}) left as performed')
sf.write(sys.argv[3],out.astype(np.float32),sr,subtype='FLOAT'); print('\n'.join(log))
