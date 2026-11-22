#!/bin/bash
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; A="python3 ../scripts/auto.py"; V=${1:-v1}
# hook lift: vocals +1.5 dB, adlibs +2.5, beat +0.5 in hooks (0:40-1:00, 2:20-2:40)
$A lead1_11lim.wav lead1_auto.wav 40-60:+1.5,140-160:+1.5
$A lead2_11lim.wav lead2_auto.wav 40-60:+1.5,140-160:+1.5
$A adlibs_11lim.wav adlibs_auto.wav 40-60:+2.5,140-160:+2.5
$A beat_enh.wav beat_auto.wav 40-60:+0.5,140-160:+0.5
$T mix mix_raw_$V.wav --track beat_auto.wav:0 --track lead1_auto.wav:${G1:-2} --track lead2_auto.wav:${G2:-1} \
  --track adlibs_auto.wav:${GA:--4} --track lead3_tel_11lim.wav:${GT:--1} \
  --track vocal_verb.wav:${GV:--4} --track adlib_delay.wav:${GD:--4} --track lead_throws.wav:${GTH:-0} | tail -1
# mix bus: light glue 2:1 (attack 20 ms, release 150 ms), then M/S: mono below 120 Hz, mid air shelf +1 dB @10k (lossy source: modest)
python3 ../scripts/glue.py mix_raw_$V.wav mix_glue_$V.wav
$T ms-bus mix_glue_$V.wav mix_ms_$V.wav --side-hp 120 --mid-shelf 10000:1.0 | tail -2
