"""Actual limiter GR: compare pre-limiter (mix -> same chain -> same gain) vs limiter output, per 10 ms block peak."""
import sys, json, subprocess, numpy as np, soundfile as sf
mix, lim = sys.argv[1], sys.argv[2]; st=json.load(open(lim+'.settings.json'))
import re; g=[float(re.search(r'volume=([-0-9.]+)dB',st['full_filtergraph']).group(1))]
chain=st.get('chain','anull') or 'anull'
subprocess.run(['ffmpeg','-v','error','-y','-i',mix,'-af',chain,'-c:a','pcm_f32le','/tmp/claude-0/-home-user-Claude-code-/b87fffa8-99f8-56f3-b136-e8a9df7d6d33/scratchpad/pre.wav'],check=True)
x,sr=sf.read('/tmp/claude-0/-home-user-Claude-code-/b87fffa8-99f8-56f3-b136-e8a9df7d6d33/scratchpad/pre.wav',always_2d=True); y,_=sf.read(lim,always_2d=True)
n=min(len(x),len(y)); x=x[:n]*10**(g[0]/20); y=y[:n]; h=int(sr*0.01); m=n//h
px=np.abs(x[:m*h]).reshape(m,-1).max(1); py=np.abs(y[:m*h]).reshape(m,-1).max(1)+1e-12
gr=20*np.log10(np.maximum(px,1e-9)/py); loud=20*np.log10(px+1e-12)>-30
print(f'{lim}: gain {g[0]:.1f} dB | GR on loudest 1% of hits {np.percentile(gr[loud],99):.1f} dB, max {gr[loud].max():.1f} dB, 90th pct {np.percentile(gr[loud],90):.1f} dB, median {np.median(gr[loud]):.1f} dB')
