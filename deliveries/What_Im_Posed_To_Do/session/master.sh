#!/bin/bash
# master: DC-block HPF -> oversampled limiter (target -13.4, ceiling -2.3) -> 12 Hz zero-phase DC block -> verses -1 dB post-limit -> trim
set -e; cd work; V=$1; MIX=${2:-mix_ms_$1.wav}
python3 ../scripts/render_master.py $MIX master_lim_$V.wav --target-lufs ${TGT:--13.4} --ceiling -2.3 --chain "highpass=f=20:poles=2" 2>&1 | grep -E "Result|WARN"
python3 ../scripts/dcblock.py master_lim_$V.wav master_dc_$V.wav | cut -c1-40
python3 ../scripts/auto.py master_dc_$V.wav master_auto_$V.wav 71.1-99.1:-1.0,157.4-174.2:-1.0 >/dev/null
python3 ../scripts/trim.py master_auto_$V.wav master_$V.wav
