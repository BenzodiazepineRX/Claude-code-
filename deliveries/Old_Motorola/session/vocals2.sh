#!/bin/bash
# v2 dynamics: harder fast stage (1176-style), then the rest of the chain as before, vocal peak limiter at -7.5 dBFS
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; F="ffmpeg -v error -y -i"
v=$1; dslo=$2; dshi=$3; tone=$4; drive=$5; mix=$6; dsp=${7:-97}; ride=${8:-}
{
$T comp2 ${v}_04dyn.wav ${v}_05comp.wav --peak-threshold -15 --peak-ratio 6 | sed -n 2,3p
$T deess ${v}_05comp.wav ${v}_06ds.wav --low $dslo --high $dshi --auto-pct $dsp | tail -1
$F ${v}_06ds.wav -af "$tone" -c:a pcm_f32le ${v}_07tone.wav
$T saturate ${v}_07tone.wav ${v}_08sat.wav --drive $drive --even 0.15 --mix $mix | tail -1
$T deess ${v}_08sat.wav ${v}_09ds2.wav --low 5500 --high 9000 --max-cut 4 --auto-pct 98.5 | tail -1
python3 ../scripts/rider.py ${v}_09ds2.wav ${v}_10ride.wav $ride
$F ${v}_10ride.wav -af "aresample=176400,alimiter=limit=-7.5dB:attack=0.5:release=40:level=disabled:asc=1,aresample=44100" -c:a pcm_f32le ${v}_11lim.wav
echo DONE
} > ../log_$v.txt 2>&1
