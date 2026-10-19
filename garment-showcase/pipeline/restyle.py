"""Restyle an approved white-tee turn: new fabric color and a new chest print, frame by frame.

No generation call. It reuses a reviewed atlas whose chest print is a filled rectangle
(the bundled lake-white-v3 take), finds that rectangle in every cell, rebuilds the fabric
underneath it, recolors the cotton by luminance and warps the new artwork into the tracked
quad. The hanger keeps its wood color. Use it for concept variants, not for real products:
a real garment needs its own anchors and turn.
"""
from pathlib import Path
import argparse, json, hashlib
import numpy as np
from PIL import Image, ImageDraw

def shift(m,dy,dx):
    out=np.zeros_like(m);h,w=m.shape
    out[max(0,dy):h+min(0,dy),max(0,dx):w+min(0,dx)]=m[max(0,-dy):h-max(0,dy),max(0,-dx):w-max(0,dx)]
    return out
def dilate(m,r):
    out=m.copy()
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            if dx*dx+dy*dy<=r*r:out|=shift(m,dy,dx)
    return out
def density(m,r):
    s=np.pad(m.astype(np.int32),((1,0),(1,0))).cumsum(0).cumsum(1);h,w=m.shape
    y0=np.clip(np.arange(h)-r,0,h);y1=np.clip(np.arange(h)+r+1,0,h);x0=np.clip(np.arange(w)-r,0,w);x1=np.clip(np.arange(w)+r+1,0,w)
    return s[y1][:,x1]-s[y0][:,x1]-s[y1][:,x0]+s[y0][:,x0]
def filled(m):
    rows=(m.cumsum(1)>0)&(m[:,::-1].cumsum(1)[:,::-1]>0);cols=(m.cumsum(0)>0)&(m[::-1].cumsum(0)[::-1]>0)
    return rows&cols

def print_mask(rgb,alpha,band):
    mx,mn=rgb.max(-1),rgb.min(-1);sat=(mx-mn)/np.maximum(mx,1e-3)
    m=(alpha>.9)&((sat>.16)|(mx<.22));m[:band[0]]=False;m[band[1]:]=False
    m&=density(m,2)>=8
    return m if m.sum()>=30 else None

def fit_line(a,b):
    """Least-squares b = k*a + c on the central 70% of samples."""
    order=np.argsort(a);a,b=a[order],b[order];n=len(a);lo,hi=int(n*.15),max(int(n*.85),int(n*.15)+2)
    k,c=np.polyfit(a[lo:hi],b[lo:hi],1);return k,c
def quad(m):
    ys,xs=np.nonzero(m);x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    rows=np.arange(y0,y1+1);cols=np.arange(x0,x1+1)
    left=np.array([np.argmax(m[y]) for y in rows]);right=np.array([m.shape[1]-1-np.argmax(m[y,::-1]) for y in rows])
    top=np.array([np.argmax(m[:,x]) for x in cols]);bottom=np.array([m.shape[0]-1-np.argmax(m[::-1,x]) for x in cols])
    lines={'left':fit_line(rows,left),'right':fit_line(rows,right)}
    if len(cols)>=6:lines|={'top':fit_line(cols,top),'bottom':fit_line(cols,bottom)}
    else:lines|={'top':(0,float(y0)),'bottom':(0,float(y1))}
    def corner(h,v):  # h: y=k x+c ; v: x=k y+c
        (a,b),(c,d)=lines[h],lines[v];x=(c*b+d)/(1-c*a);return [x,a*x+b]
    return [corner('top','left'),corner('top','right'),corner('bottom','right'),corner('bottom','left')]

def perspective(dst,src):
    rows=[];rhs=[]
    for (x,y),(u,v) in zip(dst,src):
        rows+=[[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]];rhs+=[u,v]
    return np.linalg.solve(np.array(rows,float),np.array(rhs,float)).tolist()

def polygon_mask(corners,shape,grow):
    c=np.array(corners);center=c.mean(0);d=c-center;c=center+d*(1+grow/np.maximum(np.linalg.norm(d,axis=1,keepdims=True),1))
    im=Image.new('L',(shape[1],shape[0]));ImageDraw.Draw(im).polygon([tuple(p) for p in c],fill=255);return np.asarray(im)>0

def hanger_mask(rgb,alpha,limit):
    r,g,b=rgb[...,0],rgb[...,1],rgb[...,2];mx,mn=rgb.max(-1),rgb.min(-1);sat=(mx-mn)/np.maximum(mx,1e-3)
    m=(alpha>.05)&(sat>.18)&(mx<.93);m[limit:]=False
    green=m&(g>r)&(g>b);return m,green

def recolor(cell,target,contrast,lref,fill=None,band_limit=80,wood=(.42,.27,.17)):
    rgb,alpha=cell[...,:3].copy(),cell[...,3]
    hanger,green=hanger_mask(rgb,alpha,band_limit)
    lum=rgb@np.array([.2126,.7152,.0722])
    if fill is not None:lum=np.where(fill[0],fill[1],lum);hanger&=~fill[0]
    out=np.clip(np.array(target)[None,None,:]+contrast*(lum-lref)[...,None],0,1)
    # Key residue on the wood becomes wood again, at its own luminance.
    w=np.array(wood);wood_rgb=np.clip(w[None,None,:]*(lum/(w@np.array([.2126,.7152,.0722])))[...,None],0,1)
    keep=np.where(green[...,None],wood_rgb,rgb)
    out=np.where(hanger[...,None],keep,out)
    return out,lum,hanger

def rebuild_fabric(lum,alpha,region,rng,iterations=500):
    """Harmonic fill of cotton luminance across the removed print, seeded row by row."""
    fill=lum.copy();h,w=lum.shape;ok=(alpha>.6)&~region
    def spans(grid,valid,size):
        """Linear interpolation across each line of the region, plus distance to its nearer end."""
        value=np.zeros(grid.shape);near=np.full(grid.shape,np.inf)
        for i in np.nonzero(grid.any(1))[0]:
            xs=np.nonzero(grid[i])[0];a,b=xs.min(),xs.max()
            first=[lum_t[i,x] for x in range(max(0,a-4),a) if valid[i,x]];last=[lum_t[i,x] for x in range(b+1,min(size,b+5)) if valid[i,x]]
            if not first and not last:continue
            l=np.mean(first) if first else np.mean(last);r=np.mean(last) if last else l
            t=(np.arange(a,b+1)-a+1)/(b-a+2);value[i,a:b+1]=l+(r-l)*t
            near[i,a:b+1]=np.minimum(np.arange(a,b+1)-a+1,b-np.arange(a,b+1)+1) if first and last else (np.arange(a,b+1)-a+1 if first else b-np.arange(a,b+1)+1)
        return value,near
    lum_t=lum;row,dr=spans(region,ok,w)
    lum_t=lum.T;col,dc=spans(region.T,ok.T,h);col,dc=col.T,dc.T
    # Transfinite blend: each pixel trusts the nearer pair of boundaries.
    wr,wc=1/dr**2,1/dc**2;blend=(row*wr+col*wc)/np.maximum(wr+wc,1e-12)
    fill[region]=np.where(np.isfinite(dr)|np.isfinite(dc),blend,lum)[region]
    # Relax only inside a padded window: the region never touches its edge, so roll() cannot wrap into it.
    ry,rx=np.nonzero(region);y0,y1,x0,x1=max(0,ry.min()-3),min(h,ry.max()+4),max(0,rx.min()-3),min(w,rx.max()+4)
    sub=fill[y0:y1,x0:x1];inside=region[y0:y1,x0:x1];valid=(alpha[y0:y1,x0:x1]>.6).astype(np.float64)
    # Vertical neighbors weigh more: folds on a hanging tee run top to bottom.
    steps=(((1,0),3),((-1,0),3),((0,1),1),((0,-1),1))
    count=sum(k*np.roll(valid,s,(0,1)) for s,k in steps);use=inside&(count>0)
    for _ in range(iterations):
        total=sum(k*np.roll(sub*valid,s,(0,1)) for s,k in steps)
        sub[use]=total[use]/count[use]
    # Borrow fine cotton texture from the fabric directly below the old print.
    span=ry.max()-ry.min()+3;src=np.clip(ry+span,0,h-1)
    blur=lambda a:sum(np.roll(a,(dy,dx),(0,1)) for dy in range(-3,4) for dx in range(-3,4))/49
    detail=lum-blur(lum);ok_src=alpha[src,rx]>.9
    fill[ry,rx]+=np.where(ok_src,.8*detail[src,rx],0)+rng.normal(0,.003,len(ry))
    return fill

def smooth(tracks,visible):
    out=[None]*len(tracks);idx=[i for i in range(len(tracks)) if visible[i]]
    for j,i in enumerate(idx):
        near=[tracks[k] for k in idx[max(0,j-1):j+2]];out[i]=np.mean(near,axis=0) if 0<j<len(idx)-1 else np.array(tracks[i])
    return out

def restyle(base,out,artwork,color,contrast,band,quality,label):
    manifest=json.loads((base/'manifest.json').read_text());W,H,C,N=manifest['width'],manifest['height'],manifest['columns'],manifest['frameCount']
    atlas=np.asarray(Image.open(base/manifest['atlas']).convert('RGBA')).astype(np.float64)/255
    cells=[atlas[(i//C)*H:(i//C+1)*H,(i%C)*W:(i%C+1)*W] for i in range(N)]
    target=[int(color[k:k+2],16)/255 for k in (0,2,4)];rng=np.random.default_rng(7)
    masks=[print_mask(c[...,:3],c[...,3],band) for c in cells]
    visible=[m is not None and m.sum()>=60 for m in masks]
    quads=smooth([quad(filled(m)) if v else None for m,v in zip(masks,visible)],visible)
    front=cells[-1];flum=front[...,:3]@np.array([.2126,.7152,.0722]);body=(front[...,3]>.9)&~dilate(masks[-1],3);body[:band[0]]=False
    lref=float(np.median(flum[body]))
    art=Image.open(artwork).convert('RGBA');aw,ah=art.size;S=4
    frames=[]
    for i,cell in enumerate(cells):
        region=None
        if masks[i] is not None:
            region=dilate(masks[i],3)
            if visible[i]:region|=polygon_mask(quads[i],masks[i].shape,3)
            region&=cell[...,3]>.05
        lum0=cell[...,:3]@np.array([.2126,.7152,.0722])
        fill=None if region is None else (region,rebuild_fabric(lum0,cell[...,3],region,rng))
        rgb,lum,hanger=recolor(cell,target,contrast,lref,fill)
        if visible[i]:
            q=np.array(quads[i])*S
            coeffs=perspective([tuple(p) for p in q],[(0,0),(aw,0),(aw,ah),(0,ah)])
            big=art.transform((W*S,H*S),Image.Transform.PERSPECTIVE,coeffs,Image.Resampling.BICUBIC)
            ink=np.asarray(big.resize((W,H),Image.Resampling.LANCZOS)).astype(np.float64)/255
            clip=dilate(region,1).astype(np.float64)
            shade=np.clip(1+.6*(lum-lref),.82,1.06)[...,None]
            grain=np.clip(rng.normal(.97,.03,(H,W)),.88,1)
            ia=ink[...,3]*clip*grain*(cell[...,3]>.6)
            rgb=rgb*(1-ia[...,None])+np.clip(ink[...,:3]*shade,0,1)*ia[...,None]
        frames.append(np.dstack([rgb,cell[...,3]]))
    out.mkdir(parents=True,exist_ok=False)
    sheet=Image.new('RGBA',(W*C,H*((N+C-1)//C)))
    for i,f in enumerate(frames):sheet.paste(Image.fromarray(np.rint(f*255).astype(np.uint8),'RGBA'),((i%C)*W,(i//C)*H))
    sheet.save(out/'atlas.webp',quality=quality,method=6)
    decoded=Image.open(out/'atlas.webp').convert('RGBA')
    tile=lambda i:decoded.crop(((i%C)*W,(i//C)*H,(i%C+1)*W,(i//C+1)*H))
    tile(0).save(out/'profile.webp',lossless=True,exact=True);tile(N-1).save(out/'front.webp',lossless=True,exact=True)
    back=base/'back.webp'
    if back.exists():
        b=np.asarray(Image.open(back).convert('RGBA')).astype(np.float64)/255
        blum=b[...,:3]@np.array([.2126,.7152,.0722]);bref=float(np.median(blum[(b[...,3]>.9)]))
        brgb,_,_=recolor(b,target,contrast,bref)
        Image.fromarray(np.rint(np.dstack([brgb,b[...,3]])*255).astype(np.uint8),'RGBA').save(out/'back.webp',quality=90,method=6)
    review=Image.new('RGB',(W*5,H*3))
    for row,bg in enumerate([(245,243,238),(23,33,48),(210,170,110)]):
        for col,i in enumerate([0,N//4,N//2,3*N//4,N-1]):
            t=Image.new('RGBA',(W,H),bg);t.alpha_composite(tile(i));review.paste(t.convert('RGB'),(col*W,row*H))
    review.save(out/'key-review.jpg',quality=90)
    source={'kind':'restyled-generated-video','base':base.name,'baseSha256':manifest.get('source',{}).get('sha256'),'artworkSha256':hashlib.sha256(Path(artwork).read_bytes()).hexdigest(),'fabric':'#'+color,'note':label}
    result={k:manifest[k] for k in ['version','width','height','columns','frameCount','pivot']}|{'atlas':'atlas.webp','profile':'profile.webp','front':'front.webp','source':source,'processing':{'printBand':list(band),'trackedFrames':int(sum(visible)),'contrast':contrast},'bytes':(out/'atlas.webp').stat().st_size}
    (out/'manifest.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base',type=Path,required=True,help='Reviewed fixture folder with a filled rectangular chest print')
    p.add_argument('--art',type=Path,required=True,help='RGBA artwork; transparent pixels show the fabric')
    p.add_argument('--out',type=Path,required=True);p.add_argument('--color',required=True,help='Fabric hex, e.g. 1c1c1e')
    p.add_argument('--contrast',type=float,default=.6,help='How much of the white take\'s shading carries into the new fabric')
    p.add_argument('--band',default='80,232',help='Rows that may contain the old print');p.add_argument('--quality',type=int,default=88)
    p.add_argument('--label',default='Concept variant derived from an approved take')
    a=p.parse_args()
    if a.out.exists():raise SystemExit('Output already exists. Use a new named output.')
    result=restyle(a.base,a.out,a.art,a.color.lstrip('#'),a.contrast,tuple(map(int,a.band.split(','))),a.quality,a.label)
    print(json.dumps({'output':str(a.out),'trackedFrames':result['processing']['trackedFrames'],'atlasBytes':result['bytes'],'review':'Inspect key-review.jpg and the UI turn.'},indent=2))

if __name__=='__main__':main()
