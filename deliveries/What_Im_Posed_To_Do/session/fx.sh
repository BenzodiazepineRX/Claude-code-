#!/bin/bash
# FX for "What I'm Posed To Do" — everything timed to 135 BPM
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; F="ffmpeg -v error -y -i"
# shared plate: decay = 1 bar (1.78 s), pre-delay 1/64 = 27.78 ms, return EQ 350-8k, ducked 4 dB by all vocals; BGs send +4 dB more
$T mix verbsend.wav --track lead1_11lim.wav:0 --track lead2_11lim.wav:0 --track bg1_11lim.wav:4 --track bg2_11lim.wav:4 >/dev/null
$T reverb verbsend.wav plate.wav --type plate --decay 1.78 --predelay 27.78 --hp 350 --lp 8000 --duck-by allvox.wav --duck-depth 4 | head -1 &
# ambience: 1/4 (444.44 ms) ping-pong on the leads, ducked 12 dB by all vocals
$T delay leadbus.wav amb_delay.wav --bpm 135 --note 1/4 --feedback 0.3 --hp 400 --lp 4500 --duck-by allvox.wav --duck-depth 12 | head -1 &
# BG delay: 1/8 dotted (333.33 ms) in the bridge, ducked by all vocals
$T mix bgbus.wav --track bg1_11lim.wav:0 --track bg2_11lim.wav:0 >/dev/null
$T delay bgbus.wav bg_delay.wav --bpm 135 --note 1/8d --feedback 0.35 --hp 400 --lp 5000 --duck-by allvox.wav --duck-depth 10 | head -1 &
wait
# throws (ducked by all vocals so echoes only bloom in the space)
$T delay allvox.wav thr_8d.wav --bpm 135 --note 1/8d --feedback 0.35 --hp 400 --lp 5000 --throws "45.90-46.24,102.82-103.16" --duck-by allvox.wav | head -1 &
$T delay allvox.wav thr_q.wav --bpm 135 --note 1/4 --feedback 0.4 --hp 400 --lp 5000 --throws "114.86-115.20" --duck-by allvox.wav | head -1 &
$T delay allvox.wav thr_h.wav --bpm 135 --note 1/2 --feedback 0.5 --hp 450 --lp 4500 --throws "57.94-58.28,144.15-144.55,172.70-173.20" --duck-by allvox.wav | head -1 &
# gap fills: tease + ghost (dry, phone-filtered) with their own space
$T reverb fills_dry.wav fills_verb.wav --type hall --decay 2.4 --predelay 27.78 --hp 400 --lp 6000 | head -1 &
$T delay fills_dry.wav fills_delay.wav --bpm 135 --note 1/4 --feedback 0.45 --hp 500 --lp 3500 | head -1 &
# reverse swells into hook 1 (0:42.23) and verse 2 (2:37.47): hall of the entry words, reversed
$T reverb leadbus.wav swell_wet.wav --type hall --decay 2.6 --predelay 0 --hp 300 --lp 7000 | head -1 &
wait
python3 ../scripts/revswell.py swell_wet.wav rev_swells.wav 42.23,157.47 2.0
# hook doubler: +/-7 cents, 13/19 ms, hard L/R, only in the hooks
$F leadbus.wav -af "pan=mono|c0=0.5*c0+0.5*c1,asetrate=44100*1.004052,aresample=44100,atempo=0.995964,adelay=13" -c:a pcm_f32le dblL.wav &
$F leadbus.wav -af "pan=mono|c0=0.5*c0+0.5*c1,asetrate=44100*0.995965,aresample=44100,atempo=1.004051,adelay=19" -c:a pcm_f32le dblR.wav &
wait
ffmpeg -v error -y -i dblL.wav -i dblR.wav -filter_complex "[0][1]amerge=inputs=2[a]" -map "[a]" -c:a pcm_f32le dbl_raw.wav
python3 ../scripts/auto.py dbl_raw.wav dbl_hooks.wav 0-42.0:-80,71.1-99.3:-80,128.0-200:-80 0.15
echo FX-DONE
