"""Gap fills on the full timeline: intro tease (hook-2 line 1, 4 bars before hook 1) and ghost echo (BG2's last line, 4 bars later). Telephone-filtered."""
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfiltfilt
sr=44100; bar=4*60/135; W='work/'
lead,_=sf.read(W+'leadbus.wav',always_2d=True); bg2,_=sf.read(W+'bg2_11lim.wav',always_2d=True)
L=len(lead)+int(30*sr); out=np.zeros((L,2))
def seg(x,a,b):
    s=x[int(a*sr):int(b*sr)].copy(); f=int(0.02*sr); s[:f]*=np.linspace(0,1,f)[:,None]; s[-f:]*=np.linspace(1,0,f)[:,None]; return s
def phone(s): return sosfiltfilt(butter(2,[500,3200],'band',fs=sr,output='sos'),s,axis=0)*1.6
def place(s,t,g): i=int(t*sr); out[i:i+len(s)]+=s*10**(g/20)
place(phone(seg(lead,99.05,103.30)),99.05-56.889-4*bar,-6)   # hook-2 line 1 teased 4 bars before hook 1
place(phone(seg(bg2,140.0,144.6)),140.0+4*bar,-6)             # BG2 last line echoed 4 bars later in the gap
sf.write(W+'fills_dry.wav',out.astype(np.float32),sr,subtype='FLOAT')
print(f'tease at {99.05-56.889-4*bar:.2f}s, ghost at {140.0+4*bar:.2f}s (both telephone 500-3200 Hz)')
