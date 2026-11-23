#!/bin/bash
# v15 mix: v14 tone match + lead -1.5 dB vs beat (beat +1.5), reverb -3 dB, stack -3 dB & HP 600 Hz
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; A="python3 ../scripts/auto.py"; V=${1:-v11}
LA="42.2-58.7:+1.5,58.7-65.8:-1.5,65.8-71.1:+1.5,87.1-99.1:-3,99.1-115.6:-1.5,115.6-128.0:+1.5"
$A lead1_14fin.wav lead1_auto.wav $LA >/dev/null; $A lead2_14fin.wav lead2_auto.wav $LA >/dev/null
$A plate4.wav plate4_auto.wav 58.7-65.8:+1,87.1-115.6:+1 >/dev/null
$A amb_delay.wav amb_auto.wav 42.2-71.1:+2,99.1-128:+2 >/dev/null
$T mix mix_raw_$V.wav --track beat_final2.wav:${GBEAT:-1.0} --track lead1_auto.wav:${GL:--1.9} --track lead2_auto.wav:${GL:--1.9} \
 --track bg1_pan.wav:${GB:--1.5} --track bg2_pan.wav:${GB:--1.5} --track stack4.wav:${GS:--7.0} --track plate4_auto.wav:${GV:--0.5} \
 --track amb_auto.wav:-6 --track bg_delay.wav:-6 --track thr3_8d.wav:-2 --track thr3_q.wav:-2 --track thr3_h.wav:0 \
 --track echo_bg3.wav:${GE:-8} --track bg_throws.wav:-1 --track fills_dry.wav:0 --track fills_verb.wav:-2 --track fills_delay.wav:-6 --track rev_swells.wav:-4 | tail -1
python3 ../scripts/glue.py mix_raw_$V.wav mix_glue_$V.wav
$T ms-bus mix_glue_$V.wav mix_ms_$V.wav --side-hp 120 --mid-shelf 10000:0.5 | tail -1
