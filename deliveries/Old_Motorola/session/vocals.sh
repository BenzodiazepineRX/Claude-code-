#!/bin/bash
# Old Motorola — vocal chains (v1). Order follows the Pro Mix & Master doc.
set -e; cd work; T="python3 ../scripts/dsp_tools.py"; F="ffmpeg -v error -y -i"
chain () { # name hpf staticEQ dynF dynQ dsLo dsHi toneEQ drive mix
  v=$1; echo "==================== $v"
  $T hpf ${v}_01gs.wav ${v}_02hpf.wav --freq $2 --order 3 | tail -1
  $F ${v}_02hpf.wav -af "$3" -c:a pcm_f32le ${v}_03eq.wav
  $T dyneq ${v}_03eq.wav ${v}_04dyn.wav --freq $4 --q $5 --auto-pct 96 | tail -1
  $T comp2 ${v}_04dyn.wav ${v}_05comp.wav | sed -n 2p
  $T deess ${v}_05comp.wav ${v}_06ds.wav --low $6 --high $7 --auto-pct ${DSP:-97} | tail -1
  $F ${v}_06ds.wav -af "$8" -c:a pcm_f32le ${v}_07tone.wav
  $T saturate ${v}_07tone.wav ${v}_08sat.wav --drive $9 --even 0.15 --mix ${10} | tail -1
  $T deess ${v}_08sat.wav ${v}_09ds2.wav --low 5500 --high 9000 --max-cut 4 --auto-pct 98.5 | tail -1
  python3 ../scripts/rider.py ${v}_09ds2.wav ${v}_10ride.wav ${RIDE:-}
}
chain lead1 80 "equalizer=f=433:t=q:w=6:g=-2.5,equalizer=f=579:t=q:w=6:g=-1.5,equalizer=f=300:t=q:w=1.0:g=-1.5" \
  4500 3 5000 8000 "equalizer=f=3200:t=q:w=1.0:g=2,highshelf=f=10000:g=1.5" 6 0.25
chain lead2 80 "equalizer=f=1007:t=q:w=6:g=-3.5,equalizer=f=576:t=q:w=6:g=-1.5,equalizer=f=300:t=q:w=1.0:g=-1.5" \
  4540 3 5000 8000 "equalizer=f=3200:t=q:w=1.0:g=2,highshelf=f=10000:g=1.5" 6 0.25
# adlibs: higher HPF, darker (LP 10k), more grit, harder de-ess, re-balanced pan (was 10.9 dB left -> ~5 dB left)
DSP=95 chain adlibs 150 "equalizer=f=253:t=q:w=6:g=-2,equalizer=f=3000:t=q:w=1.5:g=-1.5,lowpass=f=10000:poles=2,pan=stereo|c0=0.80*c0+0.0*c1|c1=0.35*c0+1.0*c1" \
  3055 3 5000 8000 "equalizer=f=3500:t=q:w=1.0:g=1" 9 0.35
# telephone lead: keep the artist's phone effect, tighten band (HP 300 / LP 5.5k), more grit
RIDE="--max-db 2" chain lead3_tel 300 "lowpass=f=5500:poles=2,equalizer=f=1500:t=q:w=1.0:g=1" \
  2500 2 4000 6000 "anull" 9 0.4
