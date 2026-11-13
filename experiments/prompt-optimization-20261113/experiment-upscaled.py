"""Authorized experiment. Never modifies inputs or game assets."""
import os,sys, json, hashlib, time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import cv2
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"vendor/pixel-art-fixer/python"))
from pixelfixer import detect
from pixelfixer.reconstruct import two_stage_pack, reconstruct
from pixelfixer.colorspace import srgb_to_oklab
OUT=ROOT/"results-upscaled"; OUT.mkdir(exist_ok=True)
REF=Path(os.environ.get("PS_ART_REFERENCE_DIR",str(ROOT.parents[1]/"inputs/private")))
def read(p): return np.array(Image.open(p).convert("RGBA"))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def key(a):
    a=a.copy(); x=a[:,:,:3].astype(float)
    m=(a[:,:,3]<128)|((x[:,:,1]>150)&(x[:,:,1]>1.6*x[:,:,0])&(x[:,:,1]>1.6*x[:,:,2]))
    a[:,:,3]=np.where(m,0,255); a[m,:3]=0
    return a
def native_ref(a):
    a=a.copy(); a[:,:,3]=np.where(a[:,:,3]>=128,255,0); a[a[:,:,3]==0,:3]=0
    return a
def snap(a,palette):
    a=key(a); rgb=a[:,:,:3]/255.
    lab=srgb_to_oklab(rgb); pl=srgb_to_oklab(palette/255.)
    dist=((lab[:,:,None,:]-pl[None,None,:,:])**2).sum(-1)
    a[:,:,:3]=palette[np.argmin(dist,axis=2)]
    a[a[:,:,3]==0,:3]=0
    return a
def stats(a,ref=None):
    mask=a[:,:,3]>=128
    s={"width":a.shape[1],"height":a.shape[0],"rgb":len(np.unique(a[:,:,:3][mask],axis=0)),"alpha":np.unique(a[:,:,3]).tolist(),"foreground":int(mask.sum())}
    if ref is not None and ref.shape==a.shape:
        rm=ref[:,:,3]>=128; inter=mask&rm; union=mask|rm
        s["alpha_iou"]=round(float(inter.sum()/max(1,union.sum())),4)
        s["exact_rgba_fraction"]=round(float(np.all(a==ref,axis=2).mean()),4)
        s["rgb_agreement_on_overlap"]=round(float(np.all(a[:,:,:3]==ref[:,:,:3],axis=2)[inter].mean()),4)
    return s
def save(a,name,ref=None):
    Image.fromarray(a).save(OUT/(name+".png"))
    return stats(a,ref)
def panel(im,size=(205,420)):
    p=Image.new("RGBA",size,(42,39,47,255))
    p.alpha_composite(im,(10,32))
    return p
cases=[("furnace-c",ROOT/"furnace-c-generated.png",REF/"furnace.png"),("bottle-c",ROOT/"bottle-c-generated.png",REF/"med_bottle_blue.png")]
report={"method":"RGB statistics exclude green key; original palette snapped in Oklab; no manual redrawing","source_commit":"ef376e57e1c272633ca2dbf5f29ec3fcf6596465","cases":[]}
boards=[]
# Positive control: exact 26x block copy of reference, forced recovery.
ref=native_ref(read(REF/"furnace.png"))
hi=np.repeat(np.repeat(ref,26,axis=0),26,axis=1)
cv2.setRNGSeed(42)
back=two_stage_pack(hi,48,48,k_colors=10)
report["roundtrip_control_changed_pixels"]=int(np.any(back!=ref,axis=2).sum())
for name,path,rpath in cases:
    a=read(path); ref=native_ref(read(rpath)); th,tw=ref.shape[:2]
    palette=np.unique(ref[:,:,:3][ref[:,:,3]>=128],axis=0)
    row={"name":name,"input_sha256":sha(path),"reference_sha256":sha(rpath),"raw":stats(key(a)),"target":[tw,th],"methods":{}}
    variants=[("Original",ref)]
    print("DETECT",name,flush=True)
    started=time.time(); cv2.setRNGSeed(42)
    detection=detect(a,mode="full",low_memory=True)
    row["detection"]=detection; row["detect_seconds"]=round(time.time()-started,2)
    print(json.dumps(detection),flush=True)
    cv2.setRNGSeed(42)
    auto=two_stage_pack(a,detection["cols"],detection["rows"])
    row["methods"]["auto_raw"]=save(key(auto),name+"-auto-raw")
    row["methods"]["auto_palette"]=save(snap(auto,palette),name+"-auto-palette",ref)
    nearest=np.array(Image.fromarray(a).resize((tw,th),Image.Resampling.NEAREST))
    cv2.setRNGSeed(42)
    forced=two_stage_pack(a,tw,th,k_colors=len(palette)+1)
    phased=reconstruct(a,a.shape[1]/tw,a.shape[0]/th,tw,th)
    for title,raw in [("Nearest",nearest),("Target pack",forced),("Phase snap",phased)]:
        normalized=snap(raw,palette)
        keyname=title.lower().replace(" ","-")
        row["methods"][keyname]=save(normalized,name+"-"+keyname,ref)
        variants.append((title,normalized))
    variants.append(("Auto grid",snap(auto,palette)))
    board=Image.new("RGBA",(1100,470),(42,39,47,255)); d=ImageDraw.Draw(board)
    d.text((12,8),name+" | original / reconstructed candidates; 1x and 4x; dark backdrop",fill="white")
    for i,(label,img) in enumerate(variants):
        im=Image.fromarray(img); x=12+i*218
        d.text((x,32),label+" "+str(im.size),fill="white")
        board.alpha_composite(im,(x,60))
        up=im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST)
        if up.width<=210 and up.height<=320: board.alpha_composite(up,(x,145))
        else: d.text((x,145),"Auto size too large",fill="white")
    board.convert("RGB").save(OUT/(name+"-comparison.png"))
    report["cases"].append(row)
    (OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)

