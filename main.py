from sys_tools import *

texter_compiler()

mapX,mapY,mapS = 8,8,64

global p2,p3,dr
p2=m.pi/2
p3=(3*m.pi)/2
dr=0.0174533

global spx,spy,spz,spa
spx,spy,spz,spa=4*64.0,5*64.0,20.0,0

global px,py,pdx,pdy,pa
px = 1.5*64.0
py = 6.5*64.0
pdx = 0
pdy = -1
pa = 90


a,b,c = None,door("door"),wall("brick")
mapW= [
    c,c,c,c,c,c,c,c,
    c,a,a,c,a,a,a,c,
    c,a,a,b,a,a,a,c,
    c,c,b,c,a,a,a,c,
    c,a,a,a,a,a,a,c,
    c,a,a,a,a,a,a,c,
    c,a,a,a,a,a,a,c,
    c,c,c,c,c,c,c,c,
]


global texters_sprite,wall_texters
with open("assets/sprites.json","r") as f:
    texters_sprite=json.loads(f.read())

with open("assets/walls.json","r") as f:
    wall_texters=json.loads(f.read())

def angle(x1, y1, x2, y2):
    return m.atan2(y2-y1, x2-x1)

def get_angle(x1,y1,x2,y2):
    return m.degrees(m.atan2(y2-y1, x2-x1))

def dist(ax,ay,bx,by):
    return m.sqrt((bx-ax)*(bx-ax)+(by-ay)*(by-ay))


def draw_sprite(scale,x,y,squares):
    yo=int(y-(8*scale))
    xo=int(x-(4*scale))
    rect=[]
    for s in squares:
        rect.append((xo+int(s[0]*scale),yo+int(s[1]*scale),int(s[2]*scale),int(s[3]*scale),s[4]))

    return rect

def draw_sprites(rects):
    sx=spx-px
    sy=spy-py
    sz=spz

    CS=m.cos(degToRad(pa))
    SN=m.sin(degToRad(pa))
    a=sy*CS+sx*SN
    b=sx*CS-sy*SN
    sx=a
    sy=b
    
    angle = FixAng((get_angle(degToRad(px), degToRad(py), degToRad(spx), degToRad(spy))+180)+spa)

    sx=(sx*13.0/sy)+10
    sy=(sz*30.0/sy)+8

    scale=32*16/b
    
    rect=[]

    if 315<=angle or angle<45  :rect=draw_sprite(scale*2,sx*8,sy*8,texters_sprite["soldier front stand"])
    if 225<=angle<315 :rect=draw_sprite(scale*2,sx*8,sy*8,texters_sprite["soldier Lside stand"])
    if 135<=angle<225 :rect=draw_sprite(scale*2,sx*8,sy*8,texters_sprite["soldier back stand"])
    if 45 <=angle<135 :rect=draw_sprite(scale*2,sx*8,sy*8,texters_sprite["soldier Rside stand"])
    
    

    rect.append(dist(px,py,spx,spy))
    rects.append(rect)


    return rects




def drawRays2D(rects):
    vmt=wall("brick")
    hmt=wall("brick")
    ra=(degToRad(FixAng(-pa)))-dr*40

    if ra<0: ra+=2*m.pi
    if ra>2*m.pi:ra-=2*m.pi

    for r in range(0,40):
        if ra<0: ra+=2*m.pi
        if ra>2*m.pi:ra-=2*m.pi
        distH=1000000000000000
        hx=px
        hy=py
        dof=0
        vwall=0
        hwall=0

        aTan=-1/m.tan(ra)

        if ra > m.pi:
            ry=((int(py)>>6)<<6)-0.0001
            rx=(py-ry)*aTan+px
            yo=-64
            xo=-yo*aTan

        elif ra < m.pi:
            ry=((int(py)>>6)<<6)+64
            rx=(py-ry)*aTan+px
            yo=64
            xo=-yo*aTan

        elif ra == 0 or ra == m.pi:rx=px;ry=py;dof=8
        while dof<8:
            mx=int(rx)>>6
            my=int(ry)>>6
            mp= my*mapX+mx

            if mp>0 and mp<mapX*mapY and mapW[mp]!=None:
                dof=8
                hmt=mapW[mp]


                hx=rx
                hy=ry
                distH=dist(px,py,hx,hy)
                hwall=(int(hx)-((int(hx)>>6)<<6))>>1

            else:
                rx+=xo
                ry+=yo
                dof+=1


        distV=10000000000000000000
        vx=px
        vy=py

        dof=0

        nTan=-m.tan(ra)

        if ra > p2 and ra < p3:
            rx=((int(px)>>6)<<6)-0.0001
            ry=(px-rx)*nTan+py
            xo=-64
            yo=-xo*nTan

        elif  ra < p2 or ra > p3:
            rx=((int(px)>>6)<<6)+64
            ry=(px-rx)*nTan+py
            xo=64
            yo=-xo*nTan

        else:ry=py;rx=px;dof=8
        #print()

        while dof<8:
            mx=int(rx)>>6
            my=int(ry)>>6
            mp= my*mapX+mx
            if mp>0 and mp<64 and mp<mapX*mapY and mapW[mp]!=None:
                dof=8
                vx=rx
                vy=ry
                distV=dist(px,py,vx,vy)
                vmt=mapW[mp]
                vwall=(int(vy)-((int(vy)>>6)<<6))>>1
            else:
                rx+=xo
                ry+=yo
                dof+=1



        if distV<distH:rx=vx;ry=vy;disT=distV;c=(155);tmt=vmt;wall_slice=vwall
        if distV>distH:rx=hx;ry=hy;disT=distH;c=(100);tmt=hmt;wall_slice=hwall
        #512*256
        ca=FixAng(degToRad((ra/dr)+pa))

        if ca<0:ca+=2*m.pi
        if ca>2*m.pi:ca-=2*m.pi

        disTT=disT*m.cos(ca)

        rp = int((c*(1.0/(disT/100.0)))*31/255)
        if rp <  0: rp = 0
        if rp > 31: rp = 31
        c = rp *8

        lineH=int((mapS*128)/disTT)
        lineOff = 128 - (lineH>>1)

        slice_length=lineH/31
        points=[lineOff-64+((lineOff+int(slice_length*pp))-64)-(lineOff-64) for pp in range(32)]
        wall_line=wall_texters[tmt.get_texter()][wall_slice]
        
        rect=[] 
        for wl in wall_line:
            rect.append((r*4, points[wl[0]], 4, points[wl[1]]-points[wl[0]], wl[2]))
        
        rect.append(int(disT))
        rects.append(rect)


        ra+=dr*2
    return rects



def degToRad(a):
    return a*m.pi/180.0


def FixAng(a):
    if a>359: a-=360
    if a<0: a+=360
    return a




controler=[False,False,False,False,False]

display = disp()

runing=True
while runing:
    controler = display.update(controler)

    fps = display.get_fps()

    rects = []

    if controler[4]:
        xo = 0;
        if pdx < 0: xo =- 25
        else: xo = 25
        yo = 0;
        if pdy < 0: yo =- 25
        else: yo = 25

        ipx = int(px) >> 6
        ipx_add_xo = int(px + xo) >> 6
        ipy = int(py) >> 6
        ipy_add_yo = int(py + yo) >> 6
        
        door_maybe = mapW[ipy_add_yo * mapX + ipx_add_xo]
        if door_maybe != None:
            if door_maybe.get_type() == "door": 
                mapW[ipy_add_yo * mapX + ipx_add_xo] = None

    if controler[3]:
        pa -= fps / 8; pa = FixAng(pa)
        pdx =  m.cos(degToRad(pa))
        pdy = -m.sin(degToRad(pa))

    if controler[2]:
        pa += fps / 8; pa = FixAng(pa)
        pdx = m.cos(degToRad(pa))
        pdy =-m.sin(degToRad(pa))


    xo=-1;
    if pdx<0: xo=-20
    else:xo=20

    yo=-1;
    if pdy<0: yo=-20
    else: yo=20

    ipx=int(px)>>6
    ipx_add_xo=int(px+xo)>>6
    ipx_sub_xo=int(px-xo)>>6
    ipy=int(py)>>6
    ipy_add_yo=int(py+yo)>>6
    ipy_sub_yo=int(py-yo)>>6

    if controler[0]:
        if mapW[int(ipy*mapX+ipx_add_xo)]==None: px+=pdx*(fps/5)
        if mapW[ipy_add_yo*mapY+ipx]==None: py+=pdy*(fps/5)

    if controler[1]:
        if mapW[int(ipy*mapX+ipx_sub_xo)]==None: px-=pdx*(fps/5)
        if mapW[round(ipy_sub_yo)*round(mapX)+round(ipx)]==None: py-=pdy*(fps/5)


    rects = drawRays2D(rects)
    rects = draw_sprites(rects)

    rects = sorted(rects, key=lambda rects: rects[-1],reverse=True)

    display.render(rects)
