#!/bin/bash
# master + fixed-chain alternates + null test. usage: build.sh v7
set -e; V=$1
[ "$SKIPMASTER" = 1 ] || ./master.sh $V
python3 scripts/grmeter.py work/mix_ms_$V.wav work/master_lim_$V.wav
GT=$(python3 scripts/glue.py work/mix_raw_$V.wav work/_g.wav | grep -o "thr -[0-9]*" | grep -o "\-[0-9]*")
VOL=$(python3 -c "import json,re;print(re.search(r'volume=([-0-9.]+)dB',json.load(open('work/master_lim_$V.wav.settings.json'))['full_filtergraph']).group(1))")
BUS=$(python3 -c "import soundfile as sf,numpy as np;x,_=sf.read('work/mix_raw_$V.wav');print('%.3f'%(-6-20*np.log10(abs(x).max())))")
THL=$(python3 -c "print('%.6f'%(10**($GT/20)))")
echo "fixed chain: bus $BUS dB, glue thr $GT dB (sidechain HPF 600), limiter gain $VOL dB"
export BUS VOL THL REF=master_$V.wav
VOX="lead1_auto.wav:-2.1 lead2_auto.wav:-2.1 bg1_pan.wav:-1.5 bg2_pan.wav:-1.5 stack2.wav:-4.1 plate3_auto.wav:2.5 amb_auto.wav:-6 bg_delay.wav:-6 thr_8d.wav:-2 thr_q.wav:-2 thr_h.wav:0 echo_bg.wav:7 bg_throws.wav:-1"
FILL="fills_dry.wav:0 fills_verb.wav:-2 fills_delay.wav:-6 rev_swells.wav:-4"
./alts.sh main beat_final.wav:-0.5 $VOX $FILL & ./alts.sh nofills beat_final.wav:-0.5 $VOX & ./alts.sh instrumental beat_final.wav:-0.5 & ./alts.sh acapella $VOX $FILL & ./alts.sh tvtrack beat_final.wav:-0.5 bg1_pan.wav:-1.5 bg2_pan.wav:-1.5 bg_delay.wav:-6 bg_throws.wav:-1 stack2.wav:-4.1 echo_bg.wav:7 bg_plate_auto.wav:-3 & wait
python3 -c "
import numpy as np, soundfile as sf
a,_=sf.read('work/master_$V.wav'); b,_=sf.read('work/alt_main.wav'); n=min(len(a),len(b)); d=a[:n]-b[:n]
print('NULL main vs fixed chain: residual rms %.1f dBFS'%(10*np.log10((d**2).mean()+1e-20)))"
