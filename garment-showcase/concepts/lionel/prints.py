"""Typographic chest prints for the Lionel Studio concept tees.

Each canvas covers the old chest rectangle of the lake-white-v3 take (173x97 px in the
atlas cell), rendered at 4x. Transparent pixels show the restyled cotton.
"""
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2];FONTS=ROOT/'public/fonts'
W,H=692,388
def font(name,size):return ImageFont.truetype(str(FONTS/name),size)
def fit(draw,text,face,size,width):
    while size>8 and draw.textlength(text,font=font(face,size))>width:size-=2
    return font(face,size)
def centered(draw,y,text,f,fill,spacing=0):
    if spacing:
        widths=[draw.textlength(c,font=f) for c in text];total=sum(widths)+spacing*(len(text)-1);x=(W-total)/2
        for c,w in zip(text,widths):draw.text((x,y),c,font=f,fill=fill);x+=w+spacing
    else:draw.text(((W-draw.textlength(text,font=f))/2,y),text,font=f,fill=fill)

def letsgooo(ink,accent,tag):
    im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
    f=fit(d,"LET'S GOOO",'Anton-Regular.woff',200,W*.70);bang=font('Anton-Regular.woff',f.size)
    word="LET'S GOOO";tw=d.textlength(word,font=f);bw=d.textlength('!!!',font=bang);x=(W-tw-bw)/2;y=70
    d.text((x,y),word,font=f,fill=ink);d.text((x+tw,y),'!!!',font=bang,fill=accent)
    small=font('ArchivoBlack-Regular.woff',30);centered(d,y+f.size+28,tag,small,ink,spacing=9)
    return im

def studio(ink):
    im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
    big=fit(d,'LIONEL','ArchivoBlack-Regular.woff',170,W*.66);centered(d,78,'LIONEL',big,ink)
    y=78+big.size+16;d.rectangle(((W*.24),y,(W*.76),y+5),fill=ink)
    centered(d,y+22,'STUDIO',font('ArchivoBlack-Regular.woff',40),ink,spacing=26)
    return im

def monogram(ink):
    im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
    r=150;cx,cy=W/2,H/2-6;d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=ink,width=10)
    f=font('Anton-Regular.woff',190);t='LS';d.text((cx-d.textlength(t,font=f)/2,cy-f.size*.62),t,font=f,fill=ink)
    return im

PRINTS={
    'letsgooo-bone-on-black':lambda:letsgooo((239,233,223,255),(230,59,46,255),'LIONEL STUDIO'),
    'letsgooo-brown-on-sand':lambda:letsgooo((58,40,28,255),(58,40,28,255),'LIONEL STUDIO'),
    'studio-black-on-bone':lambda:studio((22,22,22,255)),
    'monogram-cream-on-olive':lambda:monogram((236,228,206,255)),
}
if __name__=='__main__':
    out=Path(sys.argv[1] if len(sys.argv)>1 else ROOT/'work/lionel/prints');out.mkdir(parents=True,exist_ok=True)
    for name,make in PRINTS.items():make().save(out/(name+'.png'));print(out/(name+'.png'))
