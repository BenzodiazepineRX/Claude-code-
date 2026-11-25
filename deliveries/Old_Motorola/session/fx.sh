#!/bin/bash
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; F="ffmpeg -v error -y -i"
# lead bus (used as the ducking key + pocket trigger)
$T mix leadbus.wav --track lead1_10ride.wav:0 --track lead2_10ride.wav:-1 --track lead3_tel_10ride.wav:0 | tail -1
# shared reverb send: leads + more adlibs (one space for everything)
$T mix verbsend.wav --track lead1_10ride.wav:0 --track lead2_10ride.wav:-1 --track lead3_tel_10ride.wav:-4 --track adlibs_10ride.wav:+2 | tail -1
# plate: decay = half note (1.25 s @96), pre-delay = 1/64 (39.06 ms); return EQ HP 350 / LP 8k; ducked 3 dB by leads
$T reverb verbsend.wav vocal_verb.wav --type plate --decay 1.25 --predelay 39.06 --hp 350 --lp 8000 --duck-by leadbus.wav --duck-depth 3 | tail -3
# adlib delay: dotted 1/8 (468.75 ms) ping-pong, fb 0.3, filtered 400-5000, ducked 10 dB by leads
$T delay adlibs_10ride.wav adlib_delay.wav --bpm 96 --note 1/8d --feedback 0.3 --hp 400 --lp 5000 --duck-by leadbus.wav --duck-depth 10 | tail -3
# hook throws on lead line endings: quarter note (625 ms)
TH=$(python3 ../scripts/throws.py leadbus.wav); echo "throws: $TH"
$T delay leadbus.wav lead_throws.wav --bpm 96 --note 1/4 --feedback 0.35 --hp 400 --lp 5000 --throws "$TH" --duck-by leadbus.wav | tail -3
# beat: vocal-triggered pocket (mid only), then gentle static low-mid dip
python3 ../scripts/pocket.py ../src/beat.wav leadbus.wav beat_pocket.wav --freq 2800 --q 0.9 --depth 2.5
$F beat_pocket.wav -af "equalizer=f=320:t=q:w=1.0:g=-1.2" -c:a pcm_f32le beat_proc.wav
echo FX-DONE
