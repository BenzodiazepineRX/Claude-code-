#!/bin/bash
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; F="ffmpeg -v error -y -i"; v=$1
{
$T deess ${v}_05comp.wav ${v}_06ds.wav --low 5000 --high 8000 --auto-pct $2 | tail -1
$F ${v}_06ds.wav -af "$3" -c:a pcm_f32le ${v}_07tone.wav
$T saturate ${v}_07tone.wav ${v}_08sat.wav --drive $4 --even 0.15 --mix $5 | tail -1
$T deess ${v}_08sat.wav ${v}_09ds2.wav --low 5500 --high 9000 --max-cut 4 --auto-pct 98.5 | tail -1
python3 ../scripts/rider.py ${v}_09ds2.wav ${v}_10ride.wav
$F ${v}_10ride.wav -af "aresample=176400,alimiter=limit=-7.5dB:attack=0.5:release=40:level=disabled:asc=1:latency=true,aresample=44100" -c:a pcm_f32le ${v}_11lim.wav
echo DONE; } > ../log06_$v.txt 2>&1
