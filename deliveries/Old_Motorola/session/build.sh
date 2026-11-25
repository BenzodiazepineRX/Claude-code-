#!/bin/bash
# Full downstream rebuild: mix -> master -> fixed-chain alternates -> null test -> exports.  usage: build.sh v5
set -e; V=$1; D=/home/user/Claude-code-/deliveries/Old_Motorola
./mix.sh $V 2>&1 | grep -E "Mix:|glue"
./master.sh $V mix_ms_$V.wav
python3 scripts/grmeter.py work/mix_ms_$V.wav work/master_lim_$V.wav; python3 scripts/lift.py work/master_$V.wav
export VOL=$(python3 -c "import json,re;print(re.search(r'volume=([-0-9.]+)dB',json.load(open('work/master_lim_$V.wav.settings.json'))['full_filtergraph']).group(1))")
export BUS=$(python3 -c "import soundfile as sf,numpy as np;x,_=sf.read('work/mix_raw_$V.wav');print('%.3f'%(-6-20*np.log10(abs(x).max())))")
echo "fixed chain: bus $BUS dB, limiter gain $VOL dB"
sed -i "s/master_v[0-9]*.wav; echo/master_$V.wav; echo/" alts.sh
VX="lead1_auto.wav:2 lead2_auto.wav:1 adlibs_auto.wav:-4 lead3_tel_11lim.wav:-1 vocal_verb.wav:-4 adlib_delay.wav:-4 lead_throws.wav:0"
./alts.sh main beat_auto.wav:0 $VX & ./alts.sh instrumental beat_auto.wav:0 & ./alts.sh acapella $VX & ./alts.sh tvtrack beat_auto.wav:0 adlibs_auto.wav:-4 adlib_verb.wav:-4 adlib_delay.wav:-4 & wait
python3 -c "
import numpy as np, soundfile as sf
a,_=sf.read('work/master_$V.wav'); b,_=sf.read('work/alt_main.wav'); n=min(len(a),len(b)); d=a[:n]-b[:n]
print('NULL main vs fixed chain: residual rms %.1f dBFS'%(10*np.log10((d**2).mean()+1e-20)))"
mkdir -p work/exp; python3 scripts/export_master.py work/master_$V.wav --name OM --outdir work/exp --rate 44100 --also-16bit --mp3 320 2>&1 | grep -E "OK|FAIL|verified|turn"
mv work/exp/OM_24bit.wav $D/Old_Motorola_Master_${V}_24b-44k.wav; mv work/exp/OM_16bit.wav $D/Old_Motorola_Master_${V}_16b-44k.wav; mv work/exp/OM.mp3 $D/Old_Motorola_Master_${V}_320k.mp3
for n in instrumental acapella tvtrack; do N=$(echo $n | sed 's/tvtrack/TV_Track/;s/instrumental/Instrumental/;s/acapella/Acapella/'); ffmpeg -v error -y -i work/alt_$n.wav -af "aresample=osf=s32:dither_method=triangular" -c:a pcm_s24le $D/Old_Motorola_${N}_${V}_24b-44k.wav; done
python3 -c "
import numpy as np, soundfile as sf
x,sr=sf.read('work/mix_ms_$V.wav'); x=x*10**(-4/20)/abs(x).max(); sf.write('$D/Old_Motorola_Unmastered_Mix_${V}_24b-44k.wav',x,sr,subtype='PCM_24')"
echo BUILD-DONE
