import displayio
from adafruit_display_text import label
import terminalio
from digitalio import DigitalInOut
import neopixel
import graphics
import rgbmatrix
import framebufferio
import board
from adafruit_esp32spi import adafruit_esp32spi
import busio
import supervisor
import gc
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect

base_width = 64
offset=0

darkPalette = displayio.Palette(6)
darkPalette[0] = 0x311606 # download orange 49,22,6
darkPalette[1] = 0x1F323F # blue
darkPalette[2] = 0xaa5500 # brown
darkPalette[3] = 0xaa55aa # pink
darkPalette[4] = 0x323232 # grey 50,50,50
darkPalette[5] = 0xffaaaa # bottle

gfont = bitmap_font.load_font('/fonts/6x10.bdf')

group=displayio.Group()


# print("g0 mem: " + str(gc.mem_free()))

weeBmp = displayio.Bitmap(5, 7, 2)
weePalette = displayio.Palette(2)
weePalette[1] = darkPalette[1]
weePalette[0] = 0x000000
weeBmp[2,0]=weeBmp[2,1]=weeBmp[1,2]=weeBmp[2,2]=weeBmp[3,2]=weeBmp[0,3]=1
weeBmp[1,3]=weeBmp[2,3]=weeBmp[3,3]=weeBmp[4,3]=weeBmp[0,4]=weeBmp[1,4]=1
weeBmp[2,4]=weeBmp[3,4]=weeBmp[4,4]=weeBmp[0,5]=weeBmp[1,5]=weeBmp[2,5]=1
weeBmp[3,5]=weeBmp[4,5]=weeBmp[1,6]=weeBmp[2,6]=weeBmp[3,6]=1
weeTg= displayio.TileGrid(weeBmp, pixel_shader=weePalette)
weeG=displayio.Group(x=offset+2,y=0)
weeG.append(weeTg)

pooBmp = displayio.Bitmap(7, 5, 2)
pooPalette = displayio.Palette(2)
pooPalette[1] = darkPalette[2]
pooPalette[0] = 0x000000
pooBmp[3,0]=1
pooBmp[2,1]=pooBmp[3,1]=pooBmp[4,1]=1
pooBmp[1,2]=pooBmp[2,2]=pooBmp[3,2]=pooBmp[4,2]=pooBmp[5,2]=1
pooBmp[1,3]=pooBmp[2,3]=pooBmp[3,3]=pooBmp[4,3]=pooBmp[5,3]=1
pooBmp[0,4]=pooBmp[1,4]=pooBmp[2,4]=pooBmp[3,4]=pooBmp[4,4]=pooBmp[5,4]=pooBmp[6,4]=1

pooTg= displayio.TileGrid(pooBmp, pixel_shader=pooPalette)
pooG=displayio.Group(x=offset+20,y=1)
pooG.append(pooTg)

boobBmp = displayio.Bitmap(7, 7, 2)
boobPalette = displayio.Palette(2)
boobPalette[1] = darkPalette[3]
boobPalette[0] = 0x000000
boobBmp[2,0]=boobBmp[3,0]=boobBmp[4,0]=1
boobBmp[1,1]=boobBmp[5,1]=1
boobBmp[0,2]=boobBmp[6,2]=1
boobBmp[0,3]=boobBmp[3,3]=boobBmp[6,3]=1
boobBmp[0,4]=boobBmp[6,4]=1
boobBmp[1,5]=boobBmp[5,5]=1
boobBmp[2,6]=boobBmp[3,6]=boobBmp[4,6]=1

boobTg= displayio.TileGrid(boobBmp, pixel_shader=boobPalette)
boobG=displayio.Group(x=offset+1,y=24)
boobG.append(boobTg)

graphBmp = displayio.Bitmap(5, 20, 2)
graphPalette = displayio.Palette(2)
graphPalette[1] = darkPalette[3]
graphPalette[0] = 0x000000
graphBmp[0,19]=graphBmp[1,19]=graphBmp[3,19]=graphBmp[4,19]=1

graphTg= displayio.TileGrid(graphBmp, pixel_shader=graphPalette)
graphG=displayio.Group(x=offset+52,y=11)
graphG.append(graphTg)


pumpBmp = displayio.Bitmap(5, 7, 2)
pumpPalette = displayio.Palette(2)
pumpPalette[1] = darkPalette[3]
pumpPalette[0] = 0x000000
pumpBmp[1,0]=pumpBmp[2,0]=pumpBmp[3,0]=1
pumpBmp[2,1]=1
pumpBmp[2,2]=1
pumpBmp[1,3]=pumpBmp[2,3]=pumpBmp[3,3]=1
pumpBmp[1,4]=pumpBmp[2,4]=pumpBmp[3,4]=1
pumpBmp[1,5]=pumpBmp[2,5]=pumpBmp[3,5]=1
pumpBmp[1,6]=pumpBmp[2,6]=pumpBmp[3,6]=1

pumpTg= displayio.TileGrid(pumpBmp, pixel_shader=pumpPalette)
pumpG=displayio.Group(x=offset+39,y=0)
pumpG.append(pumpTg)

nappyBmp = displayio.Bitmap(6, 4, 2)
nappyPalette = displayio.Palette(2)
nappyPalette[1] = darkPalette[4]
nappyPalette[0] = 0x000000
nappyBmp[0,0]=nappyBmp[1,0]=nappyBmp[2,0]=nappyBmp[3,0]=nappyBmp[4,0]=nappyBmp[5,0]=1
nappyBmp[0,1]=nappyBmp[1,1]=nappyBmp[2,1]=nappyBmp[3,1]=nappyBmp[4,1]=nappyBmp[5,1]=1
nappyBmp[1,2]=nappyBmp[2,2]=nappyBmp[3,2]=nappyBmp[4,2]=1
nappyBmp[2,3]=nappyBmp[3,3]=1


nappyTg= displayio.TileGrid(nappyBmp, pixel_shader=nappyPalette)
nappyG=displayio.Group(x=offset+2,y=10)
nappyG.append(nappyTg)

fedBmp = displayio.Bitmap(3, 7, 2)
fedPalette = displayio.Palette(2)
fedPalette[1] = darkPalette[5]
fedPalette[0] = 0x000000
fedBmp[1,0]=1
fedBmp[1,1]=1
fedBmp[0,2]=fedBmp[1,2]=fedBmp[2,2]=1
fedBmp[0,3]=fedBmp[1,3]=fedBmp[2,3]=1
fedBmp[0,4]=fedBmp[1,4]=fedBmp[2,4]=1
fedBmp[0,5]=fedBmp[1,5]=fedBmp[2,5]=1
fedBmp[0,6]=fedBmp[1,6]=fedBmp[2,6]=1

fedTg= displayio.TileGrid(fedBmp, pixel_shader=fedPalette)
fedG=displayio.Group(x=offset+3,y=16)
fedG.append(fedTg)


dashIcons=displayio.Group()
dashIcons.append(weeG)
dashIcons.append(pooG)
dashIcons.append(boobG)
dashIcons.append(pumpG)
dashIcons.append(nappyG)
dashIcons.append(fedG)


# print("g1 mem: " + str(gc
weeLabel = label.Label(font=gfont, text='0', color=darkPalette[4])
weeLabel.anchor_point=(0.0,0.0)
weeLabel.anchored_position=(offset+10,-1)

pooLabel = label.Label(font=gfont, text='0', color=darkPalette[4])
pooLabel.anchor_point=(0.0,0.0)
pooLabel.anchored_position=(offset+29,-1)

pumpLabel = label.Label(font=gfont, text='0', color=darkPalette[4])
pumpLabel.anchor_point=(0.0,0.0)
pumpLabel.anchored_position=(offset+46,-1)

nappyLabel = label.Label(font=gfont, text='0', color=darkPalette[4])
nappyLabel.anchor_point=(0.0,0.0)
nappyLabel.anchored_position=(offset+10,7)

fedLabel = label.Label(font=gfont, text='0', color=darkPalette[4])
fedLabel.anchor_point=(0.0,0.0)
fedLabel.anchored_position=(offset+10,15)

boobTLabel = label.Label(font=gfont, text='0', color=darkPalette[4])
boobTLabel.anchor_point=(0.0,0.0)
boobTLabel.anchored_position=(offset+10,23)



dashLabels=displayio.Group()
dashLabels.append(weeLabel)
dashLabels.append(pooLabel)
dashLabels.append(pumpLabel)
dashLabels.append(nappyLabel)
dashLabels.append(fedLabel)
dashLabels.append(boobTLabel)

group.append(dashLabels)
group.append(dashIcons)
group.append(graphG)
# print("g2 mem: " + str(gc.mem_free()))


def updateDashLabel(lVal,lIndex):
    #print("d0 mem: " + str(gc.mem_free())) 
    dashLabels[lIndex].text=lVal    
    #print("d1 mem: " + str(gc.mem_free())) 

def updateGraph(left):
    graphBmp = displayio.Bitmap(5, 20, 2)
    graphPalette = displayio.Palette(2)
    graphPalette[1] = darkPalette[3]
    graphPalette[0] = 0x000000

    for x in range(0, left):
            graphBmp[0, 19-x] = 1
            graphBmp[1, 19-x] = 1
    right=20-left
    for x in range(0, right):
            graphBmp[3, 19-x] = 1
            graphBmp[4, 19-x] = 1

    graphTg= displayio.TileGrid(graphBmp, pixel_shader=graphPalette)
    graphG=displayio.Group(x=offset+52,y=11)
    graphG.append(graphTg)
    group.pop()
    group.append(graphG)

def showDisplay(display):
    display.show(group)

