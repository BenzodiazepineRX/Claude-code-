#!/bin/bash
# v14: everything derived from the reference-matched lead (lead*_14fin)
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; F="ffmpeg -v error -y -i"
$T mix leadbus_m.wav --track lead1_14fin.wav:0 --track lead2_14fin.wav:0 >/dev/null
$T mix allvox_m.wav --track lead1_14fin.wav:0 --track lead2_14fin.wav:0 --track bg1_11lim.wav:0 --track bg2_11lim.wav:0 >/dev/null
# stack (doc doubler spec), hooks only
$F leadbus_m.wav -af "pan=mono|c0=0.5*c0+0.5*c1,asetrate=44100*1.005793,aresample=44100,atempo=0.994240,adelay=11,highpass=f=350:poles=2,lowpass=f=7000:poles=2" -c:a pcm_f32le stk3L.wav &
$F leadbus_m.wav -af "pan=mono|c0=0.5*c0+0.5*c1,asetrate=44100*0.994240,aresample=44100,atempo=1.005793,adelay=17,highpass=f=350:poles=2,lowpass=f=7000:poles=2" -c:a pcm_f32le stk3R.wav &
wait
ffmpeg -v error -y -i stk3L.wav -i stk3R.wav -filter_complex "[0][1]amerge=inputs=2,acompressor=threshold=-24dB:ratio=3:attack=10:release=150:knee=4:makeup=1[a]" -map "[a]" -c:a pcm_f32le stk3_raw.wav
$T deess stk3_raw.wav stk3_ds.wav --low 5000 --high 9000 --auto-pct 93 --max-cut 10 | tail -1
python3 ../scripts/auto.py stk3_ds.wav stack3.wav 0-42.0:-80,71.1-99.1:-80,128.2-200:-80 0.12 >/dev/null
# echo BGs (every line end), throws (same placements as before), from the matched voice
R="45.94-46.29,50.79-51.14,54.39-54.74,57.94-58.29,61.92-62.27,65.51-65.86,69.30-69.65,73.11-73.46,76.15-76.50,80.28-80.63,83.14-83.49,87.06-87.41,90.53-90.88,94.50-94.85,97.51-97.86,101.58-101.93,102.92-103.27,107.70-108.05,111.31-111.66,114.85-115.20,118.84-119.19,122.43-122.78,126.21-126.56,130.02-130.37,161.60-161.95,165.57-165.92,168.52-168.87,172.66-173.01"
$T delay leadbus_m.wav echo_bg3.wav --bpm 135 --note 1/4 --feedback 0.35 --hp 300 --lp 4500 --throws "$R" --duck-by allvox_m.wav --duck-depth 6 >/dev/null 2>&1 &
$T delay allvox_m.wav thr3_8d.wav --bpm 135 --note 1/8d --feedback 0.35 --hp 400 --lp 5000 --throws "45.90-46.24,102.82-103.16" --duck-by allvox_m.wav >/dev/null 2>&1 &
$T delay allvox_m.wav thr3_q.wav --bpm 135 --note 1/4 --feedback 0.4 --hp 400 --lp 5000 --throws "114.86-115.20" --duck-by allvox_m.wav >/dev/null 2>&1 &
$T delay allvox_m.wav thr3_h.wav --bpm 135 --note 1/2 --feedback 0.5 --hp 450 --lp 4500 --throws "57.94-58.29,144.15-144.55,172.70-173.20" --duck-by allvox_m.wav >/dev/null 2>&1 &
wait
# clear plate (same v13 design) from the matched voice
$T mix verbsend4.wav --track lead1_14fin.wav:0 --track lead2_14fin.wav:0 --track stack3.wav:3 --track bg1_11lim.wav:4 --track bg2_11lim.wav:4 >/dev/null
$T reverb verbsend4.wav plate4.wav --type plate --decay 1.333 --predelay 55.56 --hp 600 --lp 7500 --duck-by allvox_m.wav --duck-depth 6 2>&1 | grep -m1 Plate
echo FX4-DONE
