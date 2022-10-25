from random import randint as rand
import math as m

class soldier:
    def __init__(self, mapW, x=4, y=5, z=20, angle=0):
        self.texters=["soldier front stand", "soldier Lside stand", "soldier back stand", "soldier Rside stand"]
        self.mapW = mapW 
        self.x = x*64
        self.y = y*64
        self.z = z
        self.pdx = 1
        self.pdy = 0
        self.angle = angle
        self.time_of_last_action = 0
        self.action_durations = 5
        self.action = "Lturn"
        self.target = 0

    def update(self, time, fps):
        self.action_durations -= time-self.time_of_last_action
        
        if self.action_durations <= 0:
            r = rand(0,100)
            
            if 0<=r<=33:
                self.action = "stand"
                self.action_durations = rand(20,100)/5
                self.time_of_last_action = time 
            
            elif 34<=r<=66:
                if rand(0,1) == 1: self.action = "Rturn"
                else: self.action = "Lturn"
                self.action_durations = rand(20,70)/5
                self.time_of_last_action = time
            
            else:
                self.action = "walk"
                self.action_durations = rand(20,60)/5
                self.time_of_last_action = time
        
        else:
            if self.action == "Lturn":
                self.angle -= fps / 4; self.angle = FixAng(self.angle)
                self.pdx =  m.cos(degToRad(self.angle))
                self.pdy = -m.sin(degToRad(self.angle))
        
            if self.action == "Rturn":
                self.angle += fps / 4; self.angle = FixAng(self.angle)
                self.pdx = m.cos(degToRad(self.angle))
                self.pdy =-m.sin(degToRad(self.angle))
        
        
            xo=-1;
            if self.pdx<0: xo=-20
            else:xo=20
        
            yo=-1;
            if self.pdy<0: yo=-20
            else: yo=20
        
            ipx=int(self.x)>>6
            ipx_add_xo=int(self.x+xo)>>6
            ipx_sub_xo=int(self.x-xo)>>6
            ipy=int(self.y)>>6
            ipy_add_yo=int(self.y+yo)>>6
            ipy_sub_yo=int(self.y-yo)>>6
        
            if self.action == "walk":
                if self.mapW[int(ipy*8+ipx_add_xo)]==None: self.x+=self.pdx*(fps/7)
                if self.mapW[ipy_add_yo*8+ipx]==None: self.y+=self.pdy*(fps/7)
        

def degToRad(a):
    return a*m.pi/180.0

def FixAng(a):
    if a>359: a-=360
    if a<0: a+=360
    return a


