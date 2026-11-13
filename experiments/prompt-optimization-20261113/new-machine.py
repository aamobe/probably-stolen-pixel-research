import os,sys,json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import cv2
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"vendor/pixel-art-fixer/python"))
from pixelfixer.reconstruct import two_stage_pack
from pixelfixer.colorspace import srgb_to_oklab
OUT=ROOT/"results-new";OUT.mkdir(exist_ok=True)
REF=Path(os.environ.get("PS_ART_REFERENCE_DIR",str(ROOT.parents[1]/"inputs/private")))
a=np.array(Image.open(ROOT/"pellet-press-generated.png").convert("RGBA"))
sources=[np.array(Image.open(REF/n).convert("RGBA")) for n in ("furnace.png","furnace_on.png")]
palette=np.unique(np.concatenate([r[:,:,:3][r[:,:,3]>=128] for r in sources]),axis=0)
cv2.setRNGSeed(42)
packed=two_stage_pack(a,48,48,k_colors=len(palette)+1)
def snap(raw):
 x=raw[:,:,:3].astype(float);key=(x[:,:,1]>150)&(x[:,:,1]>1.6*x[:,:,0])&(x[:,:,1]>1.6*x[:,:,2])
 lab=srgb_to_oklab(x/255.);pl=srgb_to_oklab(palette/255.)
 im=raw.copy();im[:,:,:3]=palette[np.argmin(((lab[:,:,None,:]-pl)**2).sum(-1),axis=2)]
 im[:,:,3]=np.where(key,0,255);im[key,:3]=0;return im
native=snap(packed)
Image.fromarray(native).save(OUT/"pellet-press-native.png")
phase=[]
for offset in (-1,0,1):
 shifted=np.pad(a,((1,1),(1,1),(0,0)),mode="edge")[1+offset:1+offset+a.shape[0],1+offset:1+offset+a.shape[1]]
 cv2.setRNGSeed(42);candidate=snap(two_stage_pack(shifted,48,48,k_colors=len(palette)+1))
 phase.append({"sourceOffsetXY":offset,"changedPixels":int(np.any(native!=candidate,axis=2).sum())})
board=Image.new("RGBA",(830,420),(42,39,47,255));d=ImageDraw.Draw(board)
for i,(title,im) in enumerate([("Original furnace",Image.fromarray(sources[0])),("New pellet press",Image.fromarray(native))]):
 x=15+i*410;d.text((x,12),title+" | native + 6x",fill="white")
 board.alpha_composite(im,(x,40));board.alpha_composite(im.resize((288,288),Image.Resampling.NEAREST),(x,108))
board.convert("RGB").save(OUT/"pellet-press-comparison.png")
record={"target":[48,48],"paletteSource":["furnace","furnace_on"],"rgb":len(np.unique(native[:,:,:3][native[:,:,3]>0],axis=0)),"alpha":np.unique(native[:,:,3]).tolist(),"rawSHA256":hashlib.sha256((ROOT/"pellet-press-generated.png").read_bytes()).hexdigest(),"outputSHA256":hashlib.sha256((OUT/"pellet-press-native.png").read_bytes()).hexdigest(),"offsetSensitivity":phase,"manualEdits":False}
(OUT/"report.json").write_text(json.dumps(record,indent=2),encoding="utf-8")
print(json.dumps(record,indent=2))

