#!/bin/bash
# "What I'm Posed To Do" vocal chain. usage: vocals.sh name hpf "staticEQ" dynF dynQ dsLo dsHi "tone" drive mix [deessPct]
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; F="ffmpeg -v error -y -i"
v=$1; dsp=${11:-97}
{
$T hpf ${v}_01gs.wav ${v}_02hpf.wav --freq $2 --order 3 | tail -1
$F ${v}_02hpf.wav -af "$3" -c:a pcm_f32le ${v}_03eq.wav
$T dyneq ${v}_03eq.wav ${v}_04dyn.wav --freq $4 --q $5 --auto-pct 96 | tail -1
$T comp2 ${v}_04dyn.wav ${v}_05comp.wav --peak-threshold -15 --peak-ratio 6 | sed -n 2p
$T deess ${v}_05comp.wav ${v}_06ds.wav --low $6 --high $7 --auto-pct $dsp | tail -1
$F ${v}_06ds.wav -af "$8" -c:a pcm_f32le ${v}_07tone.wav
$T saturate ${v}_07tone.wav ${v}_08sat.wav --drive $9 --even 0.15 --mix ${10} | tail -1
$T deess ${v}_08sat.wav ${v}_09ds2.wav --low 5500 --high 9000 --max-cut 4 --auto-pct 98.5 | tail -1
python3 ../scripts/rider.py ${v}_09ds2.wav ${v}_10ride.wav
$F ${v}_10ride.wav -af "aresample=176400,alimiter=limit=-7.5dB:attack=0.5:release=40:level=disabled:asc=1:latency=true,aresample=44100" -c:a pcm_f32le ${v}_11lim.wav
echo DONE
} > ../log_$v.txt 2>&1
