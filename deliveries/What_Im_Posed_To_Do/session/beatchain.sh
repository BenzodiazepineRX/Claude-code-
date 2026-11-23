#!/bin/bash
# beat_proc -> 808 harmonics -> 808 low-band comp -> two-band transient clip -> 8-bar outro w/ 4-bar fade
set -e; cd work
python3 ../scripts/enhance808.py beat_proc.wav beat_enh.wav --level ${EL:--7}
python3 ../scripts/lowcomp.py beat_enh.wav beat_lc.wav --thr -18
python3 ../scripts/bandclip.py beat_lc.wav beat_bclip.wav --split 250 --low-reduce 2.5 --high-reduce 6 --knee 2
python3 - <<'PY'
import numpy as np, soundfile as sf
sr=44100; x,_=sf.read('beat_bclip.wav',always_2d=True); a,b=181.333,188.444; y=x[:int((b+0.05)*sr)].copy(); i0,i1=int(a*sr),int(b*sr)
y[i0:i1]*=(np.cos(np.linspace(0,np.pi/2,i1-i0))**1.5)[:,None]; y[i1:]=0; sf.write('beat_final.wav',y.astype(np.float32),sr,subtype='FLOAT')
PY
