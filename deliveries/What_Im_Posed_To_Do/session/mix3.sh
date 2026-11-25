#!/bin/bash
# v12 mix: clear plate (1/32 pre-delay, 600 Hz HP, 6 dB duck), de-boxed lead, doc-spec doubler stack (hooks only)
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; A="python3 ../scripts/auto.py"; V=${1:-v11}
LA="42.2-58.7:+1.5,58.7-65.8:-1.5,65.8-71.1:+1.5,87.1-99.1:-3,99.1-115.6:-1.5,115.6-128.0:+1.5"
$A lead1_12clr.wav lead1_auto.wav $LA >/dev/null; $A lead2_12clr.wav lead2_auto.wav $LA >/dev/null
$A plate3.wav plate3_auto.wav 58.7-65.8:+1,87.1-115.6:+1 >/dev/null
$A amb_delay.wav amb_auto.wav 42.2-71.1:+2,99.1-128:+2 >/dev/null
$T mix mix_raw_$V.wav --track beat_final.wav:${GBEAT:--0.5} --track lead1_auto.wav:${GL:--2.1} --track lead2_auto.wav:${GL:--2.1} \
 --track bg1_pan.wav:${GB:--1.5} --track bg2_pan.wav:${GB:--1.5} --track stack2.wav:${GS:--4.1} --track plate3_auto.wav:${GV:-2.5} \
 --track amb_auto.wav:-6 --track bg_delay.wav:-6 --track thr_8d.wav:-2 --track thr_q.wav:-2 --track thr_h.wav:0 \
 --track echo_bg.wav:${GE:-7} --track bg_throws.wav:-1 --track fills_dry.wav:0 --track fills_verb.wav:-2 --track fills_delay.wav:-6 --track rev_swells.wav:-4 | tail -1
python3 ../scripts/glue.py mix_raw_$V.wav mix_glue_$V.wav
$T ms-bus mix_glue_$V.wav mix_ms_$V.wav --side-hp 120 --mid-shelf 10000:0.5 | tail -1
