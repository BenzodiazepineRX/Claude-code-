#!/bin/bash
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; A="python3 ../scripts/auto.py"; V=${1:-v1}; FILLS=${FILLS:-1}
LA="42.2-58.7:+1.5,65.8-71.1:+1.5,87.1-99.1:-1.5,115.6-128.0:+1.5"
$A lead1_11lim.wav lead1_auto.wav $LA >/dev/null; $A lead2_11lim.wav lead2_auto.wav $LA >/dev/null
$A plate.wav plate_auto.wav 58.7-65.8:+2.5,87.1-115.6:+2.5,42.2-58.7:+1,115.6-128:+1 >/dev/null
$A amb_delay.wav amb_auto.wav 42.2-71.1:+2,99.1-128:+2 >/dev/null
TR="--track beat_final.wav:0 --track lead1_auto.wav:${GL:--0.5} --track lead2_auto.wav:${GL:--0.5} --track bg1_pan.wav:${GB:--0.5} --track bg2_pan.wav:${GB:--0.5}
 --track dbl_hooks.wav:${GD:--11.5} --track plate_auto.wav:${GV:--3} --track amb_auto.wav:${GA:--6} --track bg_delay.wav:-6
 --track thr_8d.wav:-2 --track thr_q.wav:-2 --track thr_h.wav:0"
[ "$FILLS" = 1 ] && TR="$TR --track fills_dry.wav:0 --track fills_verb.wav:-2 --track fills_delay.wav:-6 --track rev_swells.wav:-4"
$T mix mix_raw_$V.wav $TR | tail -1
python3 ../scripts/glue.py mix_raw_$V.wav mix_glue_$V.wav
$T ms-bus mix_glue_$V.wav mix_ms_$V.wav --side-hp 120 --mid-shelf 10000:0.5 | tail -1
