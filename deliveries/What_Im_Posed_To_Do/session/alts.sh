#!/bin/bash
# Render a version through the EXACT bus + master chain. Needs env: BUS, THL, VOL, REF.  usage: alts.sh NAME track:gain ...
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; N=$1; shift; args=(); for t in "$@"; do args+=(--track "$t"); done
$T mix alt_${N}_raw.wav "${args[@]}" >/dev/null
ffmpeg -v error -y -i alt_${N}_raw.wav -filter_complex "[0]volume=${BUS}dB,asplit[a][b];[b]highpass=f=${SCF:-600}:poles=2[sc];[a][sc]sidechaincompress=threshold=${THL}:ratio=2:attack=20:release=150:knee=4:makeup=1" -c:a pcm_f32le alt_${N}_glue.wav
$T ms-bus alt_${N}_glue.wav alt_${N}_ms.wav --side-hp 120 --mid-shelf 10000:0.5 >/dev/null
ffmpeg -v error -y -i alt_${N}_ms.wav -af "highpass=f=20:poles=2,volume=${VOL}dB,aresample=176400:resampler=soxr,alimiter=limit=-2.500dB:attack=5.0:release=60.0:level=disabled:latency=true,aresample=44100:resampler=soxr" -c:a pcm_f32le alt_${N}_lim.wav
python3 ../scripts/dcblock.py alt_${N}_lim.wav alt_${N}_dc.wav >/dev/null
python3 ../scripts/auto.py alt_${N}_dc.wav alt_${N}_auto.wav 71.1-99.1:-1.0,157.4-174.2:-1.0 >/dev/null
python3 ../scripts/trim_to.py alt_${N}_auto.wav alt_${N}.wav $REF; echo "rendered $N"
