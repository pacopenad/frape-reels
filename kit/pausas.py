import sys, subprocess, numpy as np, wave
SR=44100; src, dst = sys.argv[1], sys.argv[2]
x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',src,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32).copy()
hop=int(0.01*SR); n=len(x)//hop
rms=np.array([np.sqrt((x[i*hop:(i+1)*hop]**2).mean()) for i in range(n)]); thr=10**(-40/20); sil=rms<thr
runs=[];i=0
while i<n:
    if sil[i]:
        j=i
        while j<n and sil[j]: j+=1
        runs.append((i,j)); i=j
    else: i+=1
MAXGAP=float(sys.argv[3]) if len(sys.argv)>3 else 0.42; TAIL=0.22; HEAD=0.16; XF=int(0.04*SR); keep=[]; pos=0
for a,b in runs:
    if a==0 or b==n or (b-a)*0.01<=MAXGAP: continue
    cut0=int((a*0.01+TAIL)*SR); cut1=int((b*0.01-HEAD)*SR)
    excess=(cut1-cut0)-int((MAXGAP-TAIL-HEAD)*SR)
    if excess<=0: continue
    mid=(cut0+cut1)//2; c0=mid-excess//2; keep.append((pos,c0)); pos=c0+excess
keep.append((pos,len(x)))
out=x[keep[0][0]:keep[0][1]].copy()
for s,e in keep[1:]:
    seg=x[s:e].copy(); f=np.linspace(0,1,XF); out[-XF:]=out[-XF:]*(1-f)+seg[:XF]*f; out=np.concatenate([out,seg[XF:]])
st=np.argmax(rms>thr); out=out[max(0,st*hop-int(0.05*SR)):]
with wave.open(dst,'w') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(out,-1,1)*32767).astype(np.int16).tobytes())
print(len(x)/SR, '->', len(out)/SR)
