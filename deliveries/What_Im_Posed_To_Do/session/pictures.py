import numpy as np, soundfile as sf, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.signal import spectrogram
sr=44100; D='/home/user/Claude-code-/deliveries/Old_Motorola/'
raw,_=sf.read('work/rough_mix_raw.wav',always_2d=True); mas,_=sf.read(D+'Old_Motorola_Master_v5_24b-44k.wav',always_2d=True)
fig=plt.figure(figsize=(14,13),facecolor='#111318'); C='#e8e6e3'
def style(ax,t):
    ax.set_facecolor('#1a1d24'); ax.set_title(t,color=C,fontsize=13,loc='left',pad=8); ax.tick_params(colors='#9aa0a6')
    for s in ax.spines.values(): s.set_color('#333')
secs=[(0,20,'Intro'),(20,40,'Verse 1'),(40,60,'HOOK'),(60,70,'Break'),(70,100,'Verse 2'),(100,111.7,'Phone\nbridge'),(111.7,125,'Instr.'),(125,140,'Verse 3'),(140,160,'HOOK'),(160,165,'')]
# 1 timeline
ax=fig.add_axes([0.1,0.80,0.86,0.14]); style(ax,'1) Song map — who sings where (96 BPM, C major)')
tr=[('LEAD 1','work/lead1_01gs.wav','#4fc3f7'),('LEAD 2','work/lead2_01gs.wav','#ffb74d'),('ADLIBS','work/adlibs_01gs.wav','#ba68c8'),('LEAD 3 (phone)','work/lead3_tel_01gs.wav','#81c784')]
for k,(nm,f,col) in enumerate(tr):
    x,_=sf.read(f,always_2d=True); m=x.mean(1); h=sr//10; n=len(m)//h; e=10*np.log10((m[:n*h].reshape(n,h)**2).mean(1)+1e-12)
    on=e>np.percentile(e[e>-80],95)-25; t=np.arange(n)/10
    ax.fill_between(t,3-k+0.1,3-k+0.9,where=on,color=col,step='mid',lw=0)
    ax.text(-2,3-k+0.5,nm,color=col,ha='right',va='center',fontsize=10)
for a,b,l in secs:
    ax.axvline(a,color='#444',lw=0.8); ax.text((a+b)/2,4.15,l,color='#ffd54f' if 'HOOK' in l else C,ha='center',fontsize=9)
ax.set_xlim(0,165); ax.set_ylim(0,4.6); ax.set_yticks([]); ax.set_xlabel('seconds',color='#9aa0a6')
# 2 waveforms
for i,(x,t,col) in enumerate([(raw,'2) BEFORE — raw stems summed (unprocessed level)','#78909c'),(mas,'3) AFTER — Old Motorola master v5 (−12.1 LUFS, −2.3 dBTP)','#4fc3f7')]):
    ax=fig.add_axes([0.1,0.57-i*0.17,0.86,0.13]); style(ax,t); m=x.mean(1); h=sr//20; n=len(m)//h; b=m[:n*h].reshape(n,h)
    tt=np.arange(n)/20; ax.fill_between(tt,b.min(1),b.max(1),color=col,lw=0); r=np.sqrt((b**2).mean(1)); ax.fill_between(tt,-r,r,color='white',alpha=0.35,lw=0)
    ax.set_xlim(0,165); ax.set_ylim(-1,1); ax.axhline(10**(-2/20),color='#ef5350',lw=0.8,ls='--'); ax.axhline(-10**(-2/20),color='#ef5350',lw=0.8,ls='--')
    ax.text(163,0.85,'−2 dBTP ceiling',color='#ef5350',ha='right',fontsize=8)
    for a,_,l in secs: ax.axvline(a,color='#444',lw=0.6)
# 4 spectrograms of hook
for i,(x,t) in enumerate([(raw,'4) BEFORE — hook spectrogram (0:45–1:00)'),(mas,'5) AFTER — hook spectrogram (0:45–1:00)')]):
    ax=fig.add_axes([0.1+i*0.45,0.08,0.41,0.26]); style(ax,t); s=x[45*sr:60*sr].mean(1)
    f,tt,S=spectrogram(s,sr,nperseg=4096,noverlap=3072); S=10*np.log10(S+1e-14); S-=S.max()
    ax.pcolormesh(tt+45,f,S,vmin=-90,vmax=0,cmap='magma',shading='auto'); ax.set_yscale('symlog',linthresh=200); ax.set_ylim(30,16000)
    ax.set_ylabel('Hz',color='#9aa0a6'); ax.set_xlabel('seconds',color='#9aa0a6')
fig.text(0.1,0.015,'Waveform: colored = peaks, white = average level. Denser white band in the AFTER = louder & more even, while peaks stay under the red ceiling.',color='#9aa0a6',fontsize=10)
plt.savefig(D+'Old_Motorola_Before_After.png',dpi=110,facecolor=fig.get_facecolor()); print('png ok')
