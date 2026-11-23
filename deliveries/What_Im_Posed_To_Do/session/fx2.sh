#!/bin/bash
# v11 FX: BG layers from the lead takes, per-line echo BGs, BG throws, audible plate, ghost-only fills
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; F="ffmpeg -v error -y -i"
(cd .. && python3 scripts/fills.py)
# --- hook/verse stack: 2 detuned, delayed doubles, darker, harder de-essed, hard L/R
$F leadbus.wav -af "pan=mono|c0=0.5*c0+0.5*c1,asetrate=44100*1.005212,aresample=44100,atempo=0.994815,adelay=21,highpass=f=200:poles=2,lowpass=f=8000:poles=2" -c:a pcm_f32le stkL.wav &
$F leadbus.wav -af "pan=mono|c0=0.5*c0+0.5*c1,asetrate=44100*0.994815,aresample=44100,atempo=1.005212,adelay=29,highpass=f=200:poles=2,lowpass=f=8000:poles=2" -c:a pcm_f32le stkR.wav &
wait
ffmpeg -v error -y -i stkL.wav -i stkR.wav -filter_complex "[0][1]amerge=inputs=2,acompressor=threshold=-24dB:ratio=3:attack=10:release=150:knee=4:makeup=1[a]" -map "[a]" -c:a pcm_f32le stk_raw.wav
$T deess stk_raw.wav stk_ds.wav --low 5000 --high 9000 --auto-pct 93 --max-cut 10 | tail -1
# hooks 0 dB, verses -5 dB (=> -6 / -11 vs lead), muted in intro, bridge, gap, outro
python3 ../scripts/auto.py stk_ds.wav stack.wav 0-42.0:-80,71.1-99.1:-5,128.2-157.3:-80,174.0-200:-80 0.12
# --- echo BGs: last 0.35 s of every lead line -> 1/4 ping-pong, ducked only 6 dB so they're heard behind you
R="45.94-46.29,50.79-51.14,54.39-54.74,57.94-58.29,61.92-62.27,65.51-65.86,69.30-69.65,73.11-73.46,76.15-76.50,80.28-80.63,83.14-83.49,87.06-87.41,90.53-90.88,94.50-94.85,97.51-97.86,101.58-101.93,102.92-103.27,107.70-108.05,111.31-111.66,114.85-115.20,118.84-119.19,122.43-122.78,126.21-126.56,130.02-130.37,161.60-161.95,165.57-165.92,168.52-168.87,172.66-173.01"
$T delay leadbus.wav echo_bg.wav --bpm 135 --note 1/4 --feedback 0.35 --hp 300 --lp 4500 --throws "$R" --duck-by allvox.wav --duck-depth 6 | head -1 &
# --- bridge BG throws: 1/4 on each BG line end, fb 0.45
$T delay bgbus.wav bg_throws.wav --bpm 135 --note 1/4 --feedback 0.45 --hp 350 --lp 5000 --throws "133.08-133.43,136.67-137.02,140.48-140.83" --duck-by allvox.wav --duck-depth 4 | head -1 &
# --- ghost-only fill FX, and the reverse swell into verse 2 only
$T reverb fills_dry.wav fills_verb.wav --type hall --decay 2.4 --predelay 27.78 --hp 400 --lp 6000 > /dev/null 2>&1 &
$T delay fills_dry.wav fills_delay.wav --bpm 135 --note 1/4 --feedback 0.45 --hp 500 --lp 3500 > /dev/null 2>&1 &
wait
python3 ../scripts/revswell.py swell_wet.wav rev_swells.wav 157.47 2.0
# --- audible plate: leads + stack (+3) + BG (+4), ducked only 2 dB
$T mix verbsend2.wav --track lead1_11lim.wav:0 --track lead2_11lim.wav:0 --track stack.wav:3 --track bg1_11lim.wav:4 --track bg2_11lim.wav:4 >/dev/null
$T reverb verbsend2.wav plate2.wav --type plate --decay 1.78 --predelay 27.78 --hp 300 --lp 8000 --duck-by allvox.wav --duck-depth 2 > /dev/null 2>&1
ffmpeg -v error -y -i bg1_11lim.wav -af "pan=stereo|c0=1.0*c0|c1=0.3*c0" -c:a pcm_f32le bg1_pan.wav
ffmpeg -v error -y -i bg2_11lim.wav -af "pan=stereo|c0=0.3*c0|c1=1.0*c0" -c:a pcm_f32le bg2_pan.wav
echo FX2-DONE
