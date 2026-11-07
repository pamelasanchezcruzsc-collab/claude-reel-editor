import json, subprocess, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
VER=sys.argv[1] if len(sys.argv)>1 else "A"
# voice segments (source seconds in b.mov)
segs=[(0.15,6.90),(7.45,14.58),(15.44,23.29),(24.02,29.78),(30.03,34.88),(35.27,40.17)]
out=[];t=0
for a,b in segs: out.append((a,b,t)); t+=b-a
TOTAL=t
def o(s):  # source->output time
    for a,b,st in out:
        if a-0.001<=s<=b+0.001: return st+s-a
    raise ValueError(s)
# visual slots on SOURCE voice times: (v0,v1,kind,args)
if VER=="A":
    vis=[(0.15,14.58,"cam",None),
     (15.44,17.92,"a",(0.3,2.8)),
     (17.92,20.11,"a",(21.0,23.2)),
     (20.11,21.63,"a",(9.0,10.5)),
     (21.63,23.29,"a",(27.6,29.3)),
     (24.02,25.47,"scr",(3.5,8.2)),
     (25.47,26.99,"scr",(8.2,14.0)),
     (26.99,28.67,"scr",(14.0,21.0)),
     (28.67,30.35,"scr",(49.0,55.5)),
     (30.35,40.17,"cam",None)]
else:  # B: whole voice-over on the screen recording
    vis=[(0.15,14.58,"cam",None),
     (15.44,17.92,"scr",(0.0,3.6)),
     (17.92,20.11,"scr",(14.0,20.0)),
     (20.11,21.63,"scr",(30.0,34.0)),
     (21.63,23.29,"scr",(42.0,46.0)),
     (24.02,25.47,"scr",(3.6,8.2)),
     (25.47,26.99,"scr",(8.2,14.0)),
     (26.99,28.67,"scr",(20.0,28.0)),
     (28.67,30.35,"scr",(49.0,55.5)),
     (30.35,40.17,"cam",None)]
files=[];layout=[]
def ov(s):  # output time for visual boundary (gaps between segs collapse)
    try: return o(s)
    except ValueError:
        for i,(a,b,st) in enumerate(out):
            if s<a: return st
        return TOTAL
for i,(v0,v1,k,arg) in enumerate(vis):
    s0,s1=ov(v0),ov(v1); d=s1-s0; f=f"pieces/{VER}{i:02d}.mp4"
    if k=="cam":
        # camera: concat source spans inside [v0,v1] in sync
        parts=[(max(a,v0),min(b,v1)) for a,b,_ in out if b>v0 and a<v1]
        fc="".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[c{j}];" for j,(a,b) in enumerate(parts))
        fc+="".join(f"[c{j}]" for j in range(len(parts)))+f"concat=n={len(parts)}:v=1:a=0,fps=30,scale=1080:1920,setsar=1[v]"
        cmd=["ffmpeg","-v","error","-y","-i","src/b.mov","-filter_complex",fc,"-map","[v]"]
    elif k=="a":
        x0,x1=arg; sp=(x1-x0)/d
        cmd=["ffmpeg","-v","error","-y","-ss",str(x0),"-t",str(x1-x0+0.1),"-i","src/a.mov","-vf",f"setpts=(PTS-STARTPTS)/{sp:.5f},fps=30,scale=1080:1920,setsar=1"]
    else:
        x0,x1=arg; sp=(x1-x0)/d
        cmd=["ffmpeg","-v","error","-y","-ss",str(x0),"-t",str(x1-x0+0.1),"-i","src/screen.mp4","-vf",f"setpts=(PTS-STARTPTS)/{sp:.5f},fps=30,scale=1080:-2,crop=1080:1920:0:150,setsar=1"]
    subprocess.run(cmd+["-t",f"{d:.3f}","-an","-c:v","libx264","-preset","veryfast","-crf","17",f],check=True)
    files.append(f); layout.append({"i":i,"kind":k,"start":round(s0,3),"end":round(s1,3),"src":arg,"speed":round((arg[1]-arg[0])/d,2) if arg else 1})
open(f"pieces/{VER}.txt","w").write("".join(f"file '{os.path.basename(x)}'\n" for x in files))
af="".join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={b-a-0.012:.3f}:d=0.012[s{j}];" for j,(a,b,_) in enumerate(out))
af+="".join(f"[s{j}]" for j in range(len(out)))+f"concat=n={len(out)}:v=0:a=1[a]"
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"pieces/{VER}.txt","-i","voice.wav","-filter_complex",af.replace("[0:a]","[1:a]"),
  "-map","0:v","-map","[a]","-c:v","libx264","-preset","veryfast","-crf","17","-c:a","aac","-b:a","256k","-ar","48000","-shortest",f"master_{VER}.mp4"],check=True)
json.dump({"segs":out,"layout":layout,"total":TOTAL},open(f"layout_{VER}.json","w"),indent=1)
for l in layout: print(l)
print("total",round(TOTAL,2))
