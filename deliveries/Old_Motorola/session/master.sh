#!/bin/bash
set -e; cd work; V=${1:-v3}; MIX=${2:-mix_ms_v2.wav}
python3 ../scripts/render_master.py $MIX master_lim_$V.wav --target-lufs -11.3 --ceiling -2.3 --chain "highpass=f=20:poles=2,equalizer=f=350:t=q:w=0.8:g=-1.0" 2>&1 | grep -E "Result|Limiter took|WARN"
python3 ../scripts/dcblock.py master_lim_$V.wav master_dc_$V.wav
python3 ../scripts/auto.py master_dc_$V.wav master_auto_$V.wav 20-40:-1.0,65-100:-1.0,125-140:-1.0
python3 ../scripts/trim.py master_auto_$V.wav master_$V.wav
