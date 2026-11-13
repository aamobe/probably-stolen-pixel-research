import os,sys,json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import cv2
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"vendor/pixel-art-fixer/python"))
from pixelfixer.reconstruct import two_stage_pack
from pixelfixer.colorspace import srgb_to_oklab
OUT=ROOT/"results"
REF=Path(os.environ.get("PS_ART_REFERENCE_DIR",str(ROOT.parents[1]/"inputs/private")))
def read(p): return np.array(Image.open(p).convert("RGBA"))
def mask(a):
 x=a[:,:,:3].astype(float)
 return (a[:,:,3]>=128)&~((x[:,:,1]>150)&(x[:,:,1]>1.6*x[:,:,0])&(x[:,:,1]>1.6*x[:,:,2]))
def bounds(m):
 y,x=np.where(m);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
def palette_snap(a,p):
 m=mask(a);lab=srgb_to_oklab(a[:,:,:3]/255.);pl=srgb_to_oklab(p/255.)
 a=a.copy();a[:,:,:3]=p[np.argmin(((lab[:,:,None,:]-pl)**2).sum(-1),axis=2)]
 a[:,:,3]=np.where(m,255,0);a[~m,:3]=0;return a
cases=[("furnace-a",ROOT.parent/"prompt-validation-20261113/furnace-a-original-template.png","furnace.png"),
("furnace-b",ROOT.parent/"prompt-validation-20261113/furnace-b-github-template.png","furnace.png"),
("bottle",ROOT/"bottle-generated.png","med_bottle_blue.png")]
records=[]
board=Image.new("RGBA",(960,600),(42,39,47,255));d=ImageDraw.Draw(board)
for row,(name,path,refname) in enumerate(cases):
 a=read(path);ref=read(REF/refname);rh,rw=ref.shape[:2]
 rm=ref[:,:,3]>=128;am=mask(a);ab=bounds(am);rb=bounds(rm)
 ax,ay,ar,ad=ab;rx,ry,rr,rd=rb
 factor=min((rr-rx)/(ar-ax),(rd-ry)/(ad-ay))
 fw=max(1,round((ar-ax)*factor));fh=max(1,round((ad-ay)*factor))
 ox=round((rx+rr-fw)/2);oy=rd-fh
 crop=a[ay:ad,ax:ar].copy()
 cv2.setRNGSeed(42)
 p=np.unique(ref[:,:,:3][rm],axis=0)
 low=two_stage_pack(crop,fw,fh,k_colors=len(p)+1)
 low=palette_snap(low,p)
 final=np.zeros_like(ref);final[oy:oy+fh,ox:ox+fw]=low
 Image.fromarray(final).save(OUT/(name+"-registered.png"))
 m=final[:,:,3]>=128;union=m|rm;inter=m&rm
 rec={"name":name,"sourceBounds":ab,"referenceBounds":rb,"placement":[ox,oy,fw,fh],"target":[rw,rh],"alpha_iou":float(inter.sum()/union.sum()),"foreground":int(m.sum()),"rgb":len(np.unique(final[:,:,:3][m],axis=0)),"exactRGBAfraction":float(np.all(final==np.where((ref[:,:,3]>=128)[:,:,None],ref,0),axis=2).mean())}
 records.append(rec)
 # comparison: original / previous forced / registered, at native & x4
 variants=[("Original",ref),("Unregistered",read(OUT/(name+"-target-pack.png"))),("Registered",final)]
 y=12+row*195;d.text((12,y),name,fill="white")
 for col,(title,img) in enumerate(variants):
  x=110+col*270
  im=Image.fromarray(img)
  d.text((x,y),title,fill="white")
  board.alpha_composite(im,(x,y+22))
  board.alpha_composite(im.resize((rw*3,rh*3),Image.Resampling.NEAREST),(x+65,y+22))
board.convert("RGB").save(OUT/"registered-comparison.png")
(OUT/"registration.json").write_text(json.dumps(records,indent=2),encoding="utf-8")
print(json.dumps(records,indent=2))

