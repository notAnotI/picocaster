import ujson, utime, framebuf, _thread
from machine import I2C, Pin, ADC, PWM, SPI
from sys import exit



class LCD_1inch8(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 160
        self.height = 128

        BL = 13
        DC = 8
        RST = 12
        MOSI = 11
        SCK = 10
        CS = 9

        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)

        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()


        self.WHITE =   0xFFFF
        self.BLACK  =  0x0000
        self.GREEN   =  0x001F
        self.BLUE    =  0xF800
        self.RED   = 0x07E0


    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def get(self):
        return self.buffer

    def sent(self,buf):
        self.buffer=buf

    def init_display(self):
        """Initialize dispaly"""
        self.rst(1)
        self.rst(0)
        self.rst(1)

        self.write_cmd(0x36);
        self.write_data(0x70);

        self.write_cmd(0x3A);
        self.write_data(0x05);

         #ST7735R Frame Rate
        self.write_cmd(0xB1);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB2);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB3);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB4); #Column inversion
        self.write_data(0x07);

        #ST7735R Power Sequence
        self.write_cmd(0xC0);
        self.write_data(0xA2);
        self.write_data(0x02);
        self.write_data(0x84);
        self.write_cmd(0xC1);
        self.write_data(0xC5);

        self.write_cmd(0xC2);
        self.write_data(0x0A);
        self.write_data(0x00);

        self.write_cmd(0xC3);
        self.write_data(0x8A);
        self.write_data(0x2A);
        self.write_cmd(0xC4);
        self.write_data(0x8A);
        self.write_data(0xEE);

        self.write_cmd(0xC5); #VCOM
        self.write_data(0x0E);

        #ST7735R Gamma Sequence
        self.write_cmd(0xe0);
        self.write_data(0x0f);
        self.write_data(0x1a);
        self.write_data(0x0f);
        self.write_data(0x18);
        self.write_data(0x2f);
        self.write_data(0x28);
        self.write_data(0x20);
        self.write_data(0x22);
        self.write_data(0x1f);
        self.write_data(0x1b);
        self.write_data(0x23);
        self.write_data(0x37);
        self.write_data(0x00);
        self.write_data(0x07);
        self.write_data(0x02);
        self.write_data(0x10);

        self.write_cmd(0xe1);
        self.write_data(0x0f);
        self.write_data(0x1b);
        self.write_data(0x0f);
        self.write_data(0x17);
        self.write_data(0x33);
        self.write_data(0x2c);
        self.write_data(0x29);
        self.write_data(0x2e);
        self.write_data(0x30);
        self.write_data(0x30);
        self.write_data(0x39);
        self.write_data(0x3f);
        self.write_data(0x00);
        self.write_data(0x07);
        self.write_data(0x03);
        self.write_data(0x10);

        self.write_cmd(0xF0); #Enable test command
        self.write_data(0x01);

        self.write_cmd(0xF6); #Disable ram power save mode
        self.write_data(0x00);

            #sleep out
        self.write_cmd(0x11);
        #DEV_Delay_ms(120);

        #Turn on the LCD display
        self.write_cmd(0x29);

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x00)
        self.write_data(0xA0)



        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x02)
        self.write_data(0x00)
        self.write_data(0x81)

        self.write_cmd(0x2C)

        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)


def colour(C):
    R=C[0]
    G=C[1]
    B=C[2]

    rp = int(R*31/255) # range 0 to 31
    if rp <  0: rp = 0
    if rp > 31: rp = 31
    r = rp *8

    gp = int(G*63/255) # range 0 - 63
    if gp <  0:  gp = 0
    if gp > 63: gp = 63
    g = 0
    if gp & 1:  g = g + 8192
    if gp & 2:  g = g + 16384
    if gp & 4:  g = g + 32768
    if gp & 8:  g = g + 1
    if gp & 16: g = g + 2
    if gp & 32: g = g + 4

    bp =int(B*31/255) # range 0 - 31
    if bp < 0: bp = 0
    if bp > 31:bp = 31
    b = bp *256
    colour = r+g+b
    return colour


def texter_compiler():
    with open("assets/sprites/sprite_texters.json","r") as f:
        pre_com_texters=ujson.loads(f.read())
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
        c_texters=[]

        for texter in texters:
            texter[0]=x(     texter[0])
            texter[1]=y(     texter[1])
            texter[2]=width( texter[2])
            texter[3]=heigth(texter[3])
            texter[4]=colour(texter[4])

            c_texters.append(texter)
        com_texters[t]=c_texters

    with open("assets/sprites.json", "w") as f:
        f.write(ujson.dumps(com_texters))

   
   
    with open("assets/walls/wall_texters.json","r") as f:
        walls=ujson.loads(f.read())
    
    texter_names=walls["texter names"]
    
    for t in texter_names:
        for l in range(len(walls[t])):
            for s in range(len(walls[t][l])):
                walls[t][l][s][2]=colour(walls[t][l][s][2])
   
    with open("assets/walls.json","w") as f:
        f.write(ujson.dumps(walls)) 





def core2(LCD,rects):
    utime.sleep_ms(1)
    for R in rects:
        for r in range(0,len(R)-1):
            LCD.fill_rect(R[r][0],R[r][1],R[r][2],R[r][3],R[r][4])
    LCD.show()
    LCD.fill(0B0110100101001010)
    _thread.exit()



class disp:
    def __init__(self):
        self.pwm = PWM(Pin(13))
        self.pwm.freq(1000)
        self.pwm.duty_u16(65535)
        self.j=0
        self.frame_time=0
        self.LCD1 = LCD_1inch8()
        self.controler=[
            Pin(2, Pin.IN, Pin.PULL_DOWN),
            Pin(4, Pin.IN, Pin.PULL_DOWN),
            Pin(3, Pin.IN, Pin.PULL_DOWN),
            Pin(6, Pin.IN, Pin.PULL_DOWN),
            Pin(5, Pin.IN, Pin.PULL_DOWN),
            Pin(0, Pin.IN, Pin.PULL_DOWN),
            Pin(1, Pin.IN, Pin.PULL_DOWN)
        ]

    def update(self,controler):
        self.frame_time = round(1/(utime.ticks_ms()/1000-self.j/1000))
        self.fps=round(utime.ticks_ms()-self.j)
        self.j = utime.ticks_ms()

        for i in range(0,5):
            if self.controler[i].value()==1:
                controler[i]=True
            else:
                controler[i]=False

        if self.controler[6].value()==1:
            utime.sleep(1)
            self.LCD1.fill(65535)
            self.LCD1.show()
            exit()

        return controler


    def render(self,rects):
        waiting=True
        while waiting:
            try:
                try:
                    utime.sleep_ms(10)
                    _thread.start_new_thread(core2, (self.LCD1,rects))
                except MemoryError:
                    pass
                waiting=False
            except OSError:
                pass

    def get_fps(self):
        return self.fps
