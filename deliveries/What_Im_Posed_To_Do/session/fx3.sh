#!/bin/bash
# v12 "clear reverb": de-boxed lead, doc-spec doubler stack, long-predelay bright plate with heavier ducking
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; F="ffmpeg -v error -y -i"
# lead de-box: -1.5 dB @ 420 Hz (Q 1.4)
for v in lead1 lead2; do $F ${v}_11lim.wav -af "equalizer=f=420:t=q:w=1.4:g=-1.5" -c:a pcm_f32le ${v}_12clr.wav & done; wait
$T mix leadbus_clr.wav --track lead1_12clr.wav:0 --track lead2_12clr.wav:0 >/dev/null
# stack: +/-10 cents, 11/17 ms (doc doubler spec 10-20 ms, 5-12 cents), HP 350 / LP 7k
$F leadbus_clr.wav -af "pan=mono|c0=0.5*c0+0.5*c1,asetrate=44100*1.005793,aresample=44100,atempo=0.994240,adelay=11,highpass=f=350:poles=2,lowpass=f=7000:poles=2" -c:a pcm_f32le stk2L.wav &
$F leadbus_clr.wav -af "pan=mono|c0=0.5*c0+0.5*c1,asetrate=44100*0.994240,aresample=44100,atempo=1.005793,adelay=17,highpass=f=350:poles=2,lowpass=f=7000:poles=2" -c:a pcm_f32le stk2R.wav &
wait
ffmpeg -v error -y -i stk2L.wav -i stk2R.wav -filter_complex "[0][1]amerge=inputs=2,acompressor=threshold=-24dB:ratio=3:attack=10:release=150:knee=4:makeup=1[a]" -map "[a]" -c:a pcm_f32le stk2_raw.wav
$T deess stk2_raw.wav stk2_ds.wav --low 5000 --high 9000 --auto-pct 93 --max-cut 10 | tail -1
python3 ../scripts/auto.py stk2_ds.wav stack2.wav 0-42.0:-80,71.1-99.1:-80,128.2-200:-80 0.12   # hooks only
# clear plate: decay 3 beats (1.333 s), pre-delay 1/32 (55.56 ms), send 600 Hz-7.5 kHz, ducked 6 dB
$T mix verbsend3.wav --track lead1_12clr.wav:0 --track lead2_12clr.wav:0 --track stack2.wav:3 --track bg1_11lim.wav:4 --track bg2_11lim.wav:4 >/dev/null
$T reverb verbsend3.wav plate3.wav --type plate --decay 1.333 --predelay 55.56 --hp 600 --lp 7500 --duck-by allvox.wav --duck-depth 6 2>&1 | grep -m1 Plate
echo FX3-DONE
