import sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfiltfilt
x,sr=sf.read(sys.argv[1],always_2d=True); y=sosfiltfilt(butter(2,12,'high',fs=sr,output='sos'),x,axis=0)
sf.write(sys.argv[2],y.astype(np.float32),sr,subtype='FLOAT'); print('dcblock 12 Hz zero-phase: DC',x.mean(0),'->',y.mean(0),' peak',20*np.log10(abs(x).max()),'->',20*np.log10(abs(y).max()))
