#!/bin/bash
# v3 tone: from the de-essed vocal (06) onward, gentler presence/air
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; F="ffmpeg -v error -y -i"
v=$1; tone=$2; drive=$3; mix=$4; ride=${5:-}
{
$F ${v}_06ds.wav -af "$tone" -c:a pcm_f32le ${v}_07tone.wav
$T saturate ${v}_07tone.wav ${v}_08sat.wav --drive $drive --even 0.15 --mix $mix | tail -1
$T deess ${v}_08sat.wav ${v}_09ds2.wav --low 5500 --high 9000 --max-cut 4 --auto-pct 98.5 | tail -1
python3 ../scripts/rider.py ${v}_09ds2.wav ${v}_10ride.wav $ride
$F ${v}_10ride.wav -af "aresample=176400,alimiter=limit=-7.5dB:attack=0.5:release=40:level=disabled:asc=1:latency=true,aresample=44100" -c:a pcm_f32le ${v}_11lim.wav
echo DONE
} > ../log3_$v.txt 2>&1
