from sys import exit
import pygame as pg
import time 

def texter_compiler():
    import json
    with open("assets/sprites/sprite_texters.json","r") as f:
        pre_com_texters=json.loads(f.read())
    x     =lambda x : x/10
    y     =lambda x : x/10
    width =lambda x : x/10
    heigth=lambda x : x/10

    texter_names=pre_com_texters["texter names"]

    com_texters={
      "texter names":texter_names
    }

    for t in texter_names:
        texters=pre_com_texters[t]
        #texters.pop("texter names")
        c_texters=[]

        for texter in texters:
            texter[0]=x(     texter[0])
            texter[1]=y(     texter[1])
            texter[2]=width( texter[2])
            texter[3]=heigth(texter[3])

            c_texters.append(texter)
        com_texters[t]=c_texters

    with open("assets/sprites.json", "w") as f:
        f.write(json.dumps(com_texters))

    with open("assets/walls/wall_texters.json","r") as f:
        walls=json.loads(f.read())
    
    with open("assets/walls.json","w") as f:
        f.write(json.dumps(walls)) 
                
                
def get_time():
    return time.perf_counter()


class disp:
    def __init__(self):
        self.display=pg.display.set_mode((960,768))
        self.screen=pg.Surface((160,128))
        self.clock=pg.time.Clock()
        self.j = 0



    def update(self, controler):
        self.frame_time = round(1/(time.perf_counter_ns()/1000000-self.j))
        self.fps=round(time.perf_counter_ns()/1000000-self.j)
        self.j = time.perf_counter_ns()/1000000

        self.screen.fill((200,200,200))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            if event.type == pg.KEYDOWN:
                if event.unicode == "w":
                    controler[0]=True
                if event.unicode == "s":
                    controler[1]=True
                if event.unicode == "a":
                    controler[2]=True
                if event.unicode == "d":
                    controler[3]=True
                if event.unicode == "e":
                    controler[4]=True

            if event.type == pg.KEYUP:
                if event.unicode == "w":
                    controler[0]=False
                if event.unicode == "s":
                    controler[1]=False
                if event.unicode == "a":
                    controler[2]=False
                if event.unicode == "d":
                    controler[3]=False
                if event.unicode == "e":
                    controler[4]=False

        return controler

    def render(self, rects):
        for R in rects:
            for r in range(0, len(R)-1):
                pg.draw.rect(self.screen, (R[r][4]), (R[r][0], R[r][1], R[r][2], R[r][3]))

        screen_r = pg.transform.scale(self.screen, (960, 768))
        screen_r_rect = screen_r.get_rect()

        self.clock.tick()

        pg.display.set_caption(f"Running at {int(self.clock.get_fps())} fps.")

        self.display.blit(screen_r, screen_r_rect)

        pg.display.flip()

    def get_fps(self):
        return self.fps
