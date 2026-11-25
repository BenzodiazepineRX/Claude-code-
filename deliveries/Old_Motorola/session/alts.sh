#!/bin/bash
# Render a version through the EXACT main bus + master settings (no re-optimizing). usage: alts.sh NAME track:gain ...
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; N=$1; shift; args=(); for t in "$@"; do args+=(--track "$t"); done
$T mix alt_${N}_raw.wav "${args[@]}" >/dev/null
ffmpeg -v error -y -i alt_${N}_raw.wav -af "volume=${BUS}dB,acompressor=threshold=-20dB:ratio=2:attack=20:release=150:knee=4:makeup=1" -c:a pcm_f32le alt_${N}_glue.wav
$T ms-bus alt_${N}_glue.wav alt_${N}_ms.wav --side-hp 120 --mid-shelf 10000:1.0 >/dev/null
ffmpeg -v error -y -i alt_${N}_ms.wav -af "highpass=f=20:poles=2,equalizer=f=350:t=q:w=0.8:g=-1.0,volume=${VOL}dB,aresample=176400:resampler=soxr,alimiter=limit=-2.500dB:attack=5.0:release=60.0:level=disabled:latency=true,aresample=44100:resampler=soxr" -c:a pcm_f32le alt_${N}_lim.wav
python3 ../scripts/dcblock.py alt_${N}_lim.wav alt_${N}_dc.wav >/dev/null
python3 ../scripts/auto.py alt_${N}_dc.wav alt_${N}_auto.wav 20-40:-1.0,65-100:-1.0,125-140:-1.0 >/dev/null
python3 ../scripts/trim_to.py alt_${N}_auto.wav alt_${N}.wav master_v5.wav; echo "rendered $N"
