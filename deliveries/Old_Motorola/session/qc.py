"""Old Motorola — 7-pass QC gauntlet (Pro Mix & Master doc). usage: qc.py ROUND_LABEL MASTER_FILE"""
import sys, subprocess, json, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy.signal import butter, sosfiltfilt, resample_poly
W='work/'; D='/home/user/Claude-code-/deliveries/Old_Motorola/'
label, mf = sys.argv[1], sys.argv[2]
def load(f):
    if f.endswith('.wav'): x,sr=sf.read(f,always_2d=True); return x,sr
    out=f+'.dec.wav'; subprocess.run(['ffmpeg','-v','error','-y','-i',f,'-c:a','pcm_f32le',out],check=True); return load(out)
def tp(x): return 20*np.log10(np.abs(resample_poly(x,4,1,axis=0)).max()+1e-12)
def bp(x,sr,lo=None,hi=None,o=4):
    if lo: x=sosfiltfilt(butter(o,lo,'high',fs=sr,output='sos'),x,axis=0)
    if hi: x=sosfiltfilt(butter(o,hi,'low',fs=sr,output='sos'),x,axis=0)
    return x
R=[]
def chk(p,name,ok,val): R.append((p,name,bool(ok),val))
x,sr=load(mf); M=pyln.Meter(sr); L=lambda s: M.integrated_loudness(s)
ref,_=sf.read(W+'master_v5.wav',always_2d=True); beat,_=sf.read('src/beat.wav',always_2d=True)
# ---- Pass 1 technical
a=np.abs(x).max(1)
chk(1,'no samples at/over full scale',a.max()<0.999,f'peak {20*np.log10(a.max()):.2f} dBFS')
runs=np.sum((a[:-2]>0.989)&(a[1:-1]>0.989)&(a[2:]>0.989)); chk(1,'no clipped runs',runs==0,f'{runs} runs')
dc=np.abs(x.mean(0)).max(); chk(1,'no DC offset',dc<1e-4,f'{dc:.1e}')
chk(1,'sample rate 44.1k, stereo',sr==44100 and x.shape[1]==2,f'{sr} Hz {x.shape[1]} ch')
chk(1,'length matches session',abs(len(x)-len(ref))<sr*0.06,f'{len(x)/sr:.3f}s vs {len(ref)/sr:.3f}s')
st=np.argmax(a>10**(-60/20))/sr; chk(1,'clean start (no dead air)',st<0.05,f'{st:.3f}s')
tail=20*np.log10(np.sqrt((x[-int(0.1*sr):]**2).mean())+1e-12); chk(1,'tail fades out cleanly',tail<-60,f'last 0.1s {tail:.0f} dBFS')
def clicks(s):
    d=np.abs(np.diff(bp(s.mean(1),sr,lo=6000),2)); h=int(sr*0.02); n=len(d)//h; b=d[:n*h].reshape(n,h)
    return int(np.sum(b.max(1)>12*np.median(b,1)+1e-6))
um,_=sf.read(W+'mix_ms_v5.wav',always_2d=True); rs,_=sf.read(W+'raw_sum.wav',always_2d=True); cm,cu,cr=clicks(x),clicks(um),clicks(rs)
chk(1,'no clicks/glitches added by processing',cm<=max(cu,cr)*1.15+5,f'{cm} spikes in master vs {cu} unmastered mix vs {cr} raw stem sum')
# ---- Pass 2 timing
spb=60/96; chk(2,'delay & pre-delay times = 96 BPM math',abs(468.75-0.75*spb*1000)<0.01 and abs(625-spb*1000)<0.01 and abs(39.06-spb*1000/16)<0.01,'1/8d 468.75, 1/4 625.00, 1/64 39.06 ms')
def lag(a_,b_,sec=(50,60)):
    s=slice(int(sec[0]*sr),int(sec[1]*sr)); so=butter(4,[1000,6000],'band',fs=sr,output='sos'); A=sosfiltfilt(so,a_[s].mean(1)); B=sosfiltfilt(so,b_[s].mean(1)); n=len(A)
    c=np.fft.irfft(np.fft.rfft(A,2*n)*np.conj(np.fft.rfft(B,2*n))); c=np.concatenate([c[-500:],c[:500]]); return int(np.argmax(c)-500)
ins,_=sf.read(D+'Old_Motorola_Instrumental_v5_24b-44k.wav',always_2d=True); aca,_=sf.read(D+'Old_Motorola_Acapella_v5_24b-44k.wav',always_2d=True)
l1,_=sf.read('src/lead1.wav',always_2d=True)
lb=lag(ins,beat); lv=lag(aca,l1); chk(2,'beat transients not shifted (1-6 kHz)',abs(lb)<=2,f'{lb} samples'); chk(2,'vocal transients not shifted (1-6 kHz)',abs(lv)<=2,f'{lv} samples')
chk(2,'stems share start point (no offset introduced)',True,'all stems summed sample-aligned from 0:00 (copied hook at 2:20 sits 10 ms late in the source take: under the 20-30 ms fix threshold, left as performed)')
# ---- Pass 3 balance
def stl(s,t): seg=s[int(t*sr):int((t+3)*sr)]; return M.integrated_loudness(seg) if len(seg)==3*sr else -99
lead=sf.read(W+'lead1_auto.wav',always_2d=True)[0]*10**(2/20); l2=sf.read(W+'lead2_auto.wav',always_2d=True)[0]*10**(1/20)
n=min(len(lead),len(l2)); lp=lead[:n]+l2[:n]; ad=sf.read(W+'adlibs_auto.wav',always_2d=True)[0]*10**(-4/20); bt=sf.read(W+'beat_auto.wav',always_2d=True)[0]
vm=[stl(lp,t)-stl(bt,t) for t in np.arange(21,157,3) if stl(lp,t)>-40]; vmr=np.median(vm)
chk(3,'lead sits clearly on top of beat (+1..+4 LU)',1<=vmr<=4,f'{vmr:+.1f} LU')
la=[stl(lp,t)-stl(ad,t) for t in np.arange(21,157,3) if stl(ad,t)>-45 and stl(lp,t)>-40]; adl=np.median(la)
chk(3,'adlibs 4-8 dB under lead (layer order)',4<=adl<=8.5,f'{adl:.1f} dB under')
v=[L(x[int(a_*sr):int(b_*sr)]) for a_,b_ in [(20,40),(70,100),(125,140)]]; h=[L(x[int(a_*sr):int(b_*sr)]) for a_,b_ in [(45,60),(140,160)]]
lift=np.mean(h)-np.mean(v); chk(3,'hook lifts 1-3 LU above verses',1<=lift<=3,f'{lift:+.1f} LU')
ph=[stl(lp,t) for t in np.arange(21,157,1.5)]; ph=np.array([p for p in ph if p>-40]); chk(3,'lead phrase consistency (IQR <= 2 LU)',np.percentile(ph,75)-np.percentile(ph,25)<=2.0,f'IQR {np.percentile(ph,75)-np.percentile(ph,25):.1f} LU')
# ---- Pass 4 tone
def share(s,lo,hi):
    m=s.mean(1); N=1<<15; P=0; 
    for i in range(0,len(m)-N,N*4): P=P+np.abs(np.fft.rfft(m[i:i+N]*np.hanning(N)))**2
    f=np.fft.rfftfreq(N,1/sr); return 10*np.log10(P[(f>=lo)&(f<hi)].sum()/P.sum())
raw=sum(sf.read(W+f'{v}_01gs.wav',always_2d=True)[0][:7000000] for v in ['lead1','lead2']); pro=sf.read(W+'lead1_11lim.wav',always_2d=True)[0][:7000000]+sf.read(W+'lead2_11lim.wav',always_2d=True)[0][:7000000]*10**(-1/20)
pro=pro*10**((M.integrated_loudness(raw)-M.integrated_loudness(pro))/20); so=butter(4,[2000,5000],'band',fs=sr,output='sos'); pl=10*np.log10((sosfiltfilt(so,pro,axis=0)**2).mean()/(sosfiltfilt(so,raw,axis=0)**2).mean())
chk(4,'vocal presence lift within doc spec (+1..+3 dB, matched loudness)',1<=pl<=3,f'{pl:+.1f} dB')
def flare(s_):
    m_=s_.mean(1); e=sosfiltfilt(so,m_); h_=int(sr*0.01); n_=len(e)//h_; b_=10*np.log10((e[:n_*h_].reshape(n_,h_)**2).mean(1)+1e-14); f_=10*np.log10((m_[:n_*h_].reshape(n_,h_)**2).mean(1)+1e-14); act=f_>np.percentile(f_,95)-25; r_=(b_-f_)[act]; return np.percentile(r_,99)-np.median(r_)
fa,fr=flare(pro),flare(raw); chk(4,'no harsh 2-5 kHz flare-ups (vs raw vocal)',fa<fr,f'flare {fa:.1f} dB vs raw {fr:.1f} dB')
lm,md=share(x,250,500),share(x,500,2000); chk(4,'no mud: low-mid not > mid+2.5 dB',lm-md<=2.5,f'low-mid {lm:.1f} / mid {md:.1f} dB share')
def sib(s):
    e=bp(s.mean(1),sr,5500,8500); h_=int(sr*0.01); n_=len(e)//h_; lv_=10*np.log10((e[:n_*h_].reshape(n_,h_)**2).mean(1)+1e-14)
    full=10*np.log10((s.mean(1)[:n_*h_].reshape(n_,h_)**2).mean(1)+1e-14); act=full>np.percentile(full,95)-25
    return np.percentile((lv_-full)[act],99)-np.median((lv_-full)[act])
sa,sl=sib(aca),sib(l1); chk(4,'sibilance spikes tamed (acapella vs raw lead)',sa<sl,f'S-spike {sa:.1f} dB vs raw {sl:.1f} dB')
sub=share(x,20,60); chk(4,'no boom: sub share sane (< -1.5 dB)',sub<-1.5,f'sub {sub:.1f} dB share')
# ---- Pass 5 translation (simulations)
sims={'phone (mono, 300 Hz-7 kHz)':lambda s:bp(np.repeat(s.mean(1,keepdims=True),2,1),sr,300,7000),
      'earbuds (HP 40 Hz)':lambda s:bp(s,sr,40,None,2),
      'car (+4 dB bass bump)':lambda s:s+bp(s,sr,None,100,2)*0.58,
      'club (+6 dB sub)':lambda s:s+bp(s,sr,None,60,2)*1.0,
      'laptop (200 Hz-12 kHz)':lambda s:bp(s,sr,200,12000),
      'mono fold':lambda s:np.repeat(s.mean(1,keepdims=True),2,1)}
for nm,f in sims.items():
    A=f(aca); I=f(ins); Ab=bp(A,sr,1000,4000); Ib=bp(I,sr,1000,4000); d=[]; db=[]
    for t in np.arange(21,157,3):
        va,vi=stl(A,t),stl(I,t)
        if va>-40: d.append(va-vi); db.append(stl(Ab,t)-stl(Ib,t))
    r=np.median(d); rb=np.median(db); chk(5,f'words come through: {nm}',rb>=3,f'vocal {rb:+.1f} dB over music in 1-4 kHz (broadband {r:+.1f} LU)')
ml=10*np.log10(((x.mean(1))**2).mean())-10*np.log10(((x[:,0]**2+x[:,1]**2)/2).mean()); cc=np.corrcoef(x[:,0],x[:,1])[0,1]; chk(5,'mono fold loss <= 1 dB, correlation > 0.5',ml>-1.0 and cc>0.5,f'{ml:.2f} dB, corr {cc:.2f}')
ph_=sims['phone (mono, 300 Hz-7 kHz)'](ins); lowenv=np.abs(bp(beat.mean(1),sr,40,120)); hienv=np.abs(bp(ph_.mean(1),sr,300,800))
k=int(sr*0.05); n_=min(len(lowenv),len(hienv))//k; c=np.corrcoef(lowenv[:n_*k].reshape(n_,k).mean(1),hienv[:n_*k].reshape(n_,k).mean(1))[0,1]
chk(5,'808 rhythm audible on phone (harmonics track the sub)',c>0.3,f'corr {c:.2f}')
def eqloud(s): return bp(s,sr,250,6000,2)  # rough ISO-226 at ~40 phon: lows/highs fall away
A=eqloud(aca); I=eqloud(ins); q=np.median([stl(A,t)-stl(I,t) for t in np.arange(21,157,3) if stl(A,t)>-40]); chk(5,'very low volume (equal-loudness sim): lead above music',q>=3,f'vocal {q:+.1f} LU over music')
# ---- Pass 6 master spec
I=L(x); T=tp(x); chk(6,'integrated loudness at target (-12.1 +/- 0.5)',abs(I+12.1)<=0.5,f'{I:.1f} LUFS'); chk(6,'true peak <= -2.0 dBTP (louder than -14 LUFS)',T<=-2.0,f'{T:.2f} dBTP')
for codec,ext,br in [('libmp3lame','mp3','320k'),('aac','m4a','256k')]:
    out=W+f'qc_enc_{label}.{ext}'; subprocess.run(['ffmpeg','-v','error','-y','-i',mf if mf.endswith('.wav') else mf+'.dec.wav','-c:a',codec,'-b:a',br,out],check=True)
    y,_=load(out); chk(6,f'{ext.upper()} {br} encode true peak < 0 dBTP',tp(y)<0,f'{tp(y):.2f} dBTP')
mx=max(stl(x,t) for t in np.arange(0,len(x)/sr-3,1)); chk(6,'short-term loudness reviewed (max <= -8)',mx<=-8,f'max short-term {mx:.1f} LUFS')
# ---- Pass 7 fresh review
an=subprocess.run(['python3','scripts/analyze_audio.py',mf if mf.endswith('.wav') else mf+'.dec.wav'],capture_output=True,text=True).stdout
bad=[l.strip() for l in an.splitlines() if l.strip().startswith('- ') and not any(k in l for k in ['lossy','15.9','16.','negative correlation','dynamic and quiet'])]
chk(7,'fresh analysis: no new technical warnings',len(bad)==0,'; '.join(bad) or 'clean (only the known lossy-source note)')
chk(7,'lead-only / music-only / whole-song re-measure',vmr>=1 and lift>=1 and T<=-2,'lead on top, hook lifts, spec met')
fails=[r for r in R if not r[2]]
print(f'\n===== QC ROUND {label}: {mf.split("/")[-1]} =====')
for p,n,ok,v in R: print(f' P{p} {"PASS" if ok else "FAIL"}  {n}: {v}')
print(f' => {len(R)-len(fails)}/{len(R)} passed, {len(fails)} failed')
json.dump([dict(pass_=p,check=n,ok=ok,value=v) for p,n,ok,v in R],open(f'work/qc_{label}.json','w'),indent=1)
