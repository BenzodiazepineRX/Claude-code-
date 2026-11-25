#!/bin/bash
# v16 mix: simple-chain lead (one surgical 480 Hz cut, gentle 15 ms comp, one de-esser), all vocal FX rebuilt from it
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; A="python3 ../scripts/auto.py"; V=${1:-v11}
LA="42.2-58.7:+1.5,58.7-65.8:-1.5,65.8-71.1:+1.5,87.1-99.1:-3,99.1-115.6:-1.5,115.6-128.0:+1.5"
$A lead1_16fin.wav lead1_auto.wav $LA >/dev/null; $A lead2_16fin.wav lead2_auto.wav $LA >/dev/null
$A plate5.wav plate5_auto.wav 58.7-65.8:+1,87.1-115.6:+1 >/dev/null
$A amb_delay.wav amb_auto.wav 42.2-71.1:+2,99.1-128:+2 >/dev/null
$T mix mix_raw_$V.wav --track beat_final2.wav:${GBEAT:-1.0} --track lead1_auto.wav:${GL:-4.0} --track lead2_auto.wav:${GL:-4.0} \
 --track bg1_pan.wav:${GB:--1.5} --track bg2_pan.wav:${GB:--1.5} --track stack5.wav:${GS:--4.0} --track plate5_auto.wav:${GV:-4.9} \
 --track amb_auto.wav:-6 --track bg_delay.wav:-6 --track thr5_8d.wav:-2 --track thr5_q.wav:-2 --track thr5_h.wav:0 \
 --track echo_bg5.wav:${GE:-13.4} --track bg_throws.wav:-1 --track fills_dry.wav:0 --track fills_verb.wav:-2 --track fills_delay.wav:-6 --track rev_swells.wav:-4 | tail -1
python3 ../scripts/glue.py mix_raw_$V.wav mix_glue_$V.wav
$T ms-bus mix_glue_$V.wav mix_ms_$V.wav --side-hp 120 --mid-shelf 10000:0.5 | tail -1
