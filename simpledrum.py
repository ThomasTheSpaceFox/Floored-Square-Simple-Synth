#!/usr/bin/env python
import pygame.event
import pygame.key
import pygame.display
import pygame.image
import pygame.mixer
import pygame
from pygame.locals import *
import time
import os
import array
import math
import copy
import random
from threading import Thread
pygame.display.init()

windowicon=pygame.image.load("fssdl32.png")
pygame.display.set_icon(windowicon)
screensurf=pygame.display.set_mode((570, 550))
print (pygame.display.list_modes()[0])
pygame.display.set_caption("Untitled - Floored Square Simple Drum Loop", "Untitled - Floored Square Simple Drum Loop")
pygame.font.init()

simplefont = pygame.font.SysFont(None, 22)
iconhud=pygame.image.load("fssdl.png").convert()

#controls the frequency of the synthesizer logic and pygame mixer.
#lower frequencies are faster, but are lower quality.

versioninfo="v2.9"
copyrightinfo="Copyright (c) 2016-2018 Thomas Leathers and contributors"

synthfreq=22050
#synthfreq=16000
#synthfreq=11025
#synthfreq=8000

synthfreqmain=synthfreq

STACKRANGE=int(synthfreqmain/1)
pival=math.pi

pygame.mixer.init(frequency=synthfreq , size=-16)
pygame.mixer.set_num_channels(8)

def foobsin(num):
	return (math.floor(math.sin(num)) * 4500)


def foobtangent(num):
	return (math.floor(math.tan(num)) * 4500)
	
class drum:
	def __init__(self, tone, fade, style=0, notearray=None):
		self.tone=tone
		if notearray==None:
			if style==1:
				self.notearray=array.array('f', [(foobtangent(2.0 * pival * (self.tone) * t / synthfreq)) for t in xrange(0, STACKRANGE)])
			else:
				self.notearray=array.array('f', [(foobsin(2.0 * pival * (self.tone) * t / synthfreq)) for t in xrange(0, STACKRANGE)])
		else:
			self.notearray=notearray
		self.sample=pygame.mixer.Sound(self.notearray)
		self.fade=fade
		self.style=style
	def play(self):
		self.sample.play(-1)
		self.sample.fadeout(self.fade)
	def setfade(self, fade):
		self.fade=fade
	def setvol(self, vol):
		self.sample.set_volume(vol)
	#copy is used by the cell class to avoid recalculating the drums 15 times.
	def copy(self):
		return drum(self.tone, self.fade, self.style, notearray=self.notearray)

class cymbal:
	def __init__(self, fade, notearray=None):
		if notearray==None:
			self.notearray=array.array('f', [(random.uniform(-0.3, 0.3)) for t in xrange(0, STACKRANGE)])
		else:
			self.notearray=notearray
		self.sample=pygame.mixer.Sound(self.notearray)
		self.fade=fade
	def play(self):
		self.sample.play(-1)
		self.sample.fadeout(self.fade)
	def setfade(self, fade):
		self.fade=fade
	def setvol(self, vol):
		self.sample.set_volume(vol)
	#copy is used by the cell class to avoid recalculating the cymbal 15 times.
	def copy(self):
		return cymbal(self.fade, notearray=self.notearray)

#bass.play()
#time.sleep(0.3)


#crash=cymbal(400)

#snare.play()
#time.sleep(0.3)

snare=drum(110, 250)
bass=drum(55, 250)
hithat=cymbal(250)
tanbass=drum(27.5, 250, 1)
tansnare=drum(55, 250, 1)

class beatcell:
	def __init__(self, xoff, drumid, cellid, active=1, yoff=20):
		#samples
		self.snare=snare.copy()
		self.bass=bass.copy()
		self.cymbal=hithat.copy()
		self.tanbass=tanbass.copy()
		self.tansnare=tansnare.copy()
		
		self.vol=1.0
		self.fade=250
		self._setvols_()
		self._setfade_()
		self.mainrect=pygame.Rect(xoff, yoff, 60, 360)
		self.actlight=pygame.Rect(xoff+3, yoff+2, 54, 10)
		self.interrlight=pygame.Rect(xoff+3, yoff+14, 54, 35)
		self.padjump=38
		self.padheight=34
		pyoff=yoff+20
		self.drum0=pygame.Rect(xoff+3, pyoff+self.padjump*1, 54, self.padheight)
		self.drum1=pygame.Rect(xoff+3, pyoff+self.padjump*2, 54, self.padheight)
		self.drum2=pygame.Rect(xoff+3, pyoff+self.padjump*3, 54, self.padheight)
		self.drum3=pygame.Rect(xoff+3, pyoff+self.padjump*4, 54, self.padheight)
		self.tan_sine=pygame.Rect(xoff+3, pyoff+self.padjump*5, 54, self.padheight)
		
		self.volrot=pygame.Rect(xoff+3, pyoff+self.padjump*6, 54, self.padheight)
		self.volup=pygame.Rect(xoff+3, pyoff+self.padjump*6, 54, self.padheight//2)
		self.voldown=pygame.Rect(xoff+3, int(pyoff+self.padjump*6)+19, 54, self.padheight//2)
		
		self.faderot=pygame.Rect(xoff+3, pyoff+self.padjump*7, 54, self.padheight)
		self.fadeup=pygame.Rect(xoff+3, pyoff+self.padjump*7, 54, self.padheight//2)
		self.fadedown=pygame.Rect(xoff+3, int(pyoff+self.padjump*7)+18, 54, self.padheight//2)
		
		self.play=0
		self.active=active
		self.drumid=drumid
		self.cellid=cellid
		self.xoff=xoff
		self.yoff=yoff
		self.Goff=xoff
		self.ts=0
		if self.cellid>48:
			self.label1=simplefont.render(str(self.cellid), True, (0, 0, 0), (160, 160, 180))
		elif self.cellid>32:
			self.label1=simplefont.render(str(self.cellid), True, (255, 255, 255), (60, 30, 60))
		elif self.cellid>16:
			self.label1=simplefont.render(str(self.cellid), True, (0, 0, 0), (180, 180, 180))
		else:
			self.label1=simplefont.render(str(self.cellid), True, (255, 255, 255), (30, 30, 30))
		self.activeoff=simplefont.render("cell off", True, (255, 255, 255), (40, 0, 0))
		self.activeon=simplefont.render("cell on", True, (255, 255, 255), (255, 0, 0))
		self.d0on=simplefont.render("Quiet", True, (255, 255, 255), (0, 150, 150))
		self.d0off=simplefont.render("Quiet", True, (255, 255, 255), (0, 0, 0))
		self.d1on=simplefont.render("Bass", True, (255, 255, 255), (0, 150, 150))
		self.d1off=simplefont.render("Bass", True, (255, 255, 255), (0, 0, 0))
		self.d2on=simplefont.render("Snare", True, (255, 255, 255), (0, 150, 150))
		self.d2off=simplefont.render("Snare", True, (255, 255, 255), (0, 0, 0))
		self.d3on=simplefont.render("hithat", True, (255, 255, 255), (0, 150, 150))
		self.d3off=simplefont.render("hithat", True, (255, 255, 255), (0, 0, 0))
		self.tstan=simplefont.render("tan", True, (255, 255, 255), (150, 0, 150))
		self.tssine=simplefont.render("sine", True, (255, 255, 255), (75, 75, 150))
		self.voluplabel=simplefont.render("volume", True, (255, 255, 255), (75, 75, 150))
		self.fadetitle=simplefont.render("fade", True, (255, 255, 255), (75, 75, 150))
	def reset(self):
		self.drumid=0
		self.active=0
		self.vol=1.0
		self.fade=250
		self.ts=0
		self._setvols_()
		self._setfade_()
		self.play=0
	def changexoff(self, xoff):
		xoff=xoff+self.Goff
		yoff=self.yoff
		self.mainrect=pygame.Rect(xoff, yoff, 60, 360)
		self.actlight=pygame.Rect(xoff+3, yoff+2, 54, 10)
		self.interrlight=pygame.Rect(xoff+3, yoff+14, 54, 35)
		self.padjump=38
		self.padheight=34
		pyoff=yoff+20
		
		self.drum0=pygame.Rect(xoff+3, pyoff+self.padjump*1, 54, self.padheight)
		self.drum1=pygame.Rect(xoff+3, pyoff+self.padjump*2, 54, self.padheight)
		self.drum2=pygame.Rect(xoff+3, pyoff+self.padjump*3, 54, self.padheight)
		self.drum3=pygame.Rect(xoff+3, pyoff+self.padjump*4, 54, self.padheight)
		self.tan_sine=pygame.Rect(xoff+3, pyoff+self.padjump*5, 54, self.padheight)
		
		self.volrot=pygame.Rect(xoff+3, pyoff+self.padjump*6, 54, self.padheight)
		self.volup=pygame.Rect(xoff+3, pyoff+self.padjump*6, 54, self.padheight//2)
		self.voldown=pygame.Rect(xoff+3, int(pyoff+self.padjump*6)+19, 54, self.padheight//2)
		
		self.faderot=pygame.Rect(xoff+3, pyoff+self.padjump*7, 54, self.padheight)
		self.fadeup=pygame.Rect(xoff+3, pyoff+self.padjump*7, 54, self.padheight//2)
		self.fadedown=pygame.Rect(xoff+3, int(pyoff+self.padjump*7)+18, 54, self.padheight//2)
		self.xoff=xoff
		self.yoff=yoff
	def clickevent(self, pos, button=1):
		if self.interrlight.collidepoint(pos):
			if self.active==1:
				self.active=0
			else:
				self.active=1
		if self.tan_sine.collidepoint(pos):
			if self.ts==1:
				self.ts=0
			else:
				self.ts=1
		if self.drum0.collidepoint(pos):
			self.drumid=0
		if self.drum1.collidepoint(pos):
			self.drumid=1
		if self.drum2.collidepoint(pos):
			self.drumid=2
		if self.drum3.collidepoint(pos):
			self.drumid=3
		if self.volrot.collidepoint(pos):
			if button==4 or (self.volup.collidepoint(pos) and button==1):
				self.vol+=0.1
				if self.vol>1.0:
					self.vol=1.0
				self._setvols_()
			if button==5 or (self.voldown.collidepoint(pos) and button==1):
				self.vol-=0.1
				if self.vol<0.1:
					self.vol=0.1
				self._setvols_()
		if self.faderot.collidepoint(pos):
			if button==4 or (self.fadeup.collidepoint(pos) and button==1):
				self.fade+=50
				self._setfade_()
			if button==5 or (self.fadedown.collidepoint(pos) and button==1):
				if self.fade!=50:
					self.fade-=50
					self._setfade_()
		
	def render(self):
		if self.cellid>48:
			pygame.draw.rect(screensurf, (160, 160, 180), self.mainrect)
		
		elif self.cellid>32:
			pygame.draw.rect(screensurf, (60, 30, 60), self.mainrect)
		elif self.cellid>16:
			pygame.draw.rect(screensurf, (180, 180, 180), self.mainrect)
		else:
			pygame.draw.rect(screensurf, (30, 30, 30), self.mainrect)
		screensurf.blit(self.label1, ((self.xoff+29)-(self.label1.get_width()//2), self.yoff+330))
		if self.play==1:
			pygame.draw.rect(screensurf, (0, 255, 0), self.actlight)
		else:
			pygame.draw.rect(screensurf, (0, 40, 0), self.actlight)
		if self.active==1:
			pygame.draw.rect(screensurf, (255, 0, 0), self.interrlight)
			screensurf.blit(self.activeon, (self.interrlight.x+2, self.interrlight.y+2))
		else:
			pygame.draw.rect(screensurf, (40, 0, 0), self.interrlight)
			screensurf.blit(self.activeoff, (self.interrlight.x+2, self.interrlight.y+2))
		
		if self.drumid==0:
			pygame.draw.rect(screensurf, (0, 150, 150), self.drum0)
			screensurf.blit(self.d0on, (self.drum0.x+2, self.drum0.y+2))
		else:
			pygame.draw.rect(screensurf, (0, 0, 0), self.drum0)
			screensurf.blit(self.d0off, (self.drum0.x+2, self.drum0.y+2))
		if self.drumid==1:
			pygame.draw.rect(screensurf, (0, 150, 150), self.drum1)
			screensurf.blit(self.d1on, (self.drum1.x+2, self.drum1.y+2))
		else:
			pygame.draw.rect(screensurf, (0, 0, 0), self.drum1)
			screensurf.blit(self.d1off, (self.drum1.x+2, self.drum1.y+2))
		if self.drumid==2:
			pygame.draw.rect(screensurf, (0, 150, 150), self.drum2)
			screensurf.blit(self.d2on, (self.drum2.x+2, self.drum2.y+2))
		else:
			pygame.draw.rect(screensurf, (0, 0, 0), self.drum2)
			screensurf.blit(self.d2off, (self.drum2.x+2, self.drum2.y+2))
		if self.drumid==3:
			pygame.draw.rect(screensurf, (0, 150, 150), self.drum3)
			screensurf.blit(self.d3on, (self.drum3.x+2, self.drum3.y+2))
		else:
			pygame.draw.rect(screensurf, (0, 0, 0), self.drum3)
			screensurf.blit(self.d3off, (self.drum3.x+2, self.drum3.y+2))
		if self.ts==1:
			pygame.draw.rect(screensurf, (150, 0, 150), self.tan_sine)
			screensurf.blit(self.tstan, (self.tan_sine.x+2, self.tan_sine.y+2))
		else:
			pygame.draw.rect(screensurf, (75, 75, 150), self.tan_sine)
			screensurf.blit(self.tssine, (self.tan_sine.x+2, self.tan_sine.y+2))
		
		pygame.draw.rect(screensurf, (75, 75, 150), self.volup)
		pygame.draw.rect(screensurf, (120, 0, 120), self.voldown)
		screensurf.blit(self.voluplabel, (self.volup.x, self.volup.y))
		screensurf.blit(self.volume, (self.voldown.x, self.voldown.y))
		pygame.draw.rect(screensurf, (75, 75, 150), self.fadeup)
		pygame.draw.rect(screensurf, (120, 0, 120), self.fadedown)
		
		screensurf.blit(self.fadetitle, (self.fadeup.x, self.fadeup.y-1))
		screensurf.blit(self.fadelabel, (self.fadedown.x, self.fadedown.y))
		pygame.draw.rect(screensurf, (255, 255, 255), self.faderot, 1)
		pygame.draw.rect(screensurf, (255, 255, 255), self.volrot, 1)
	def _setvols_(self):
		self.volume=simplefont.render(str(self.vol), True, (255, 255, 255), (120, 0, 120))
		self.bass.setvol(self.vol)
		self.snare.setvol(self.vol)
		self.cymbal.setvol(self.vol)
		self.tanbass.setvol(self.vol)
		self.tansnare.setvol(self.vol)
	def _setfade_(self):
		self.fadelabel=simplefont.render(str(self.fade), True, (255, 255, 255), (120, 0, 120))
		self.bass.setfade(self.fade)
		self.snare.setfade(self.fade)
		self.cymbal.setfade(self.fade)
		self.tanbass.setfade(self.fade)
		self.tansnare.setfade(self.fade)
	def drumprocess(self):
		if self.active==0:
			return 1
		else:
			if self.ts==0:
				if self.drumid==1:
					self.bass.play()
				elif self.drumid==2:
					self.snare.play()
				elif self.drumid==3:
					self.cymbal.play()
			else:
				if self.drumid==1:
					self.tanbass.play()
				elif self.drumid==2:
					self.tansnare.play()
				elif self.drumid==3:
					self.cymbal.play()
				return 0
	



playtones=1
pygame.display.update()

celllist=[]
xoff=10
for cell in range(1, 65):
	celllist.extend([beatcell(xoff, 0, cell, 0)])
	xoff+=70

timefraction=4

def bpmdecode(beatspermin):
	return (60.0/beatspermin/timefraction)
BPM=120
waittime=bpmdecode(BPM)
progactive=1
bpmup=pygame.Rect(2, 420, 60, 40)
displaymode=pygame.Rect(90, 420, 90, 40)
bpmdown=pygame.Rect(2, 490, 60, 40)
cpbup=pygame.Rect(190, 420, 60, 40)
cpbdown=pygame.Rect(190, 490, 60, 40)

loadbx=pygame.Rect(280, 490, 70, 40)
savebx=pygame.Rect(280, 420, 70, 40)

volup=pygame.Rect(370, 420, 70, 40)
voldown=pygame.Rect(370, 490, 70, 40)

scrollbar=pygame.Rect(0, 370, 1130, 40)

cpbuplabel=simplefont.render("CPB +1", True, (255, 255, 255), (30, 30, 160))
cpbdownlabel=simplefont.render("CPB -1", True, (255, 255, 255), (30, 30, 160))

loadlabel=simplefont.render("Load(F3)", True, (255, 255, 255), (30, 30, 160))
savelabel=simplefont.render("Save(F2)", True, (255, 255, 255), (30, 30, 160))

bpmuplabel=simplefont.render("BPM +5", True, (255, 255, 255), (30, 30, 160))

bpmdownlabel=simplefont.render("BPM -5", True, (255, 255, 255), (30, 30, 160))


#chanlist=[]
#for f in [0, 1, 2, 3, 4, 5, 6, 7]:
	 #chanlist.extend([pygame.mixer.Channel(f)])
#def setvols():
	#global chanlist
	#for f in chanlist:
		#f.set_volume(mainvolume)
	#return

voldownlabel=simplefont.render("vol-", True, (255, 255, 255), (30, 30, 160))

voluplabel=simplefont.render("vol+", True, (255, 255, 255), (30, 30, 160))

dispm0=simplefont.render("use 8 cells", True, (255, 255, 255), (30, 30, 160))
dispm1=simplefont.render("use 16 cells", True, (255, 255, 255), (30, 30, 160))
dispm2=simplefont.render("use 32 cells", True, (255, 255, 255), (30, 30, 160))
dispm3=simplefont.render("use 64 cells", True, (255, 255, 255), (30, 30, 160))

scrollbarmesage2=simplefont.render("32 cell mode. Use scrollwheel over this bar and 1 & 2 keys to navigate.", True, (255, 255, 255), (120, 120, 120))
scrollbarmesage3=simplefont.render("64 cell mode. Use scrollwheel over this bar and 1, 2, 3 & 4 keys to navigate.", True, (255, 255, 255), (120, 120, 140))



def sideprocess():
	global BPM
	global waittime
	global progactive
	global screensurf
	global dispmode
	global timefraction
	global gotocell
	global mainvolume
	global celloffset
	print("starting event handler thread...")
	while progactive==1:
		screensurf.fill((60, 60, 60))
		if dispmode==2:
			pygame.draw.rect(screensurf, (120, 120, 120), scrollbar)
			screensurf.blit(scrollbarmesage2, (screensurf.get_width()//2-scrollbarmesage2.get_width()//2, scrollbar.y+20))
		if dispmode==3:
			pygame.draw.rect(screensurf, (120, 120, 140), scrollbar)
			screensurf.blit(scrollbarmesage3, (screensurf.get_width()//2-scrollbarmesage2.get_width()//2, scrollbar.y+20))
		hudiconrect=screensurf.blit(iconhud, (screensurf.get_width()-68, screensurf.get_height()-68))
		time.sleep(0.05)
		#call render routines of cells
		for cell in celllist:
			if dispmode==0 and cell.cellid>8:
				break
			if dispmode==1 and cell.cellid>16:
				break
			if dispmode==2 and cell.cellid>32:
				break
			if dispmode==3 and cell.cellid>64:
				break
			if cell.xoff>=0:
				cell.render()
		#box drawing
		pygame.draw.rect(screensurf, (30, 30, 160), bpmup)
		pygame.draw.rect(screensurf, (30, 30, 160), bpmdown)
		pygame.draw.rect(screensurf, (30, 30, 160), cpbup)
		pygame.draw.rect(screensurf, (30, 30, 160), cpbdown)
		pygame.draw.rect(screensurf, (30, 30, 160), displaymode)
		pygame.draw.rect(screensurf, (30, 30, 160), loadbx)
		pygame.draw.rect(screensurf, (30, 30, 160), savebx)
		
		#pygame.draw.rect(screensurf, (30, 30, 160), volup)
		#pygame.draw.rect(screensurf, (30, 30, 160), voldown)
		#labels
		bpmlabel=simplefont.render(str(BPM), True, (255, 255, 255), (60, 60, 60))
		#vollabel=simplefont.render(str(mainvolume), True, (255, 255, 255), (60, 60, 60))
		cpblabel=simplefont.render("Cells/Beat "+str(timefraction), True, (255, 255, 255), (60, 60, 60))
		screensurf.blit(bpmuplabel, (bpmup.x+2, bpmup.y+2))
		screensurf.blit(bpmdownlabel, (bpmdown.x+2, bpmdown.y+2))
		screensurf.blit(bpmlabel, (bpmup.x+2, bpmup.y+42))
		screensurf.blit(cpbuplabel, (cpbup.x+2, cpbup.y+2))
		screensurf.blit(cpbdownlabel, (cpbdown.x+2, cpbdown.y+2))
		screensurf.blit(cpblabel, (cpbup.x+2, cpbup.y+42))
		screensurf.blit(loadlabel, (loadbx.x+2, loadbx.y+2))
		screensurf.blit(savelabel, (savebx.x+2, savebx.y+2))
		
		#screensurf.blit(voluplabel, (volup.x+2, volup.y+2))
		#screensurf.blit(vollabel, (volup.x+2, volup.y+42))
		#screensurf.blit(voldownlabel, (voldown.x+2, voldown.y+2))
		if dispmode==1:
			screensurf.blit(dispm2, (displaymode.x+2, displaymode.y+2))
		elif dispmode==2:
			screensurf.blit(dispm3, (displaymode.x+2, displaymode.y+2))
		elif dispmode==3:
			screensurf.blit(dispm0, (displaymode.x+2, displaymode.y+2))
		else:
			screensurf.blit(dispm1, (displaymode.x+2, displaymode.y+2))
		pygame.display.update()
		#event processor
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				progactive=0
			if event.type == KEYDOWN and event.key == K_F2:
				nameret=nameloader("Type or double click file to save to:")
				if nameret!=None and nameret:
					if not os.path.isfile(nameret):
						rthmsave(nameret)
					else:
						if YNpop("file: \"" + nameret + "\"exists. overwrite?"):
							rthmsave(nameret)
			if event.type == KEYDOWN and event.key == K_F3:
				#rthmload("test.rthm")
				nameret=nameloader("Type or double click file to load:")
				if nameret!=None:
					rthmload(nameret)
			if event.type == KEYDOWN and (event.key == K_1 or event.key == K_KP1):
				if dispmode>1:
					celloffset=0
					for f in celllist:
						#this IS CORRECT. upon initalization the cells store their origional offsets to maintain placement order!
						f.changexoff(celloffset)
			if event.type == KEYDOWN and (event.key == K_2 or event.key == K_KP2):
				if dispmode>1:
					celloffset=-(70*16)
					for f in celllist:
						#this IS CORRECT. upon initalization the cells store their origional offsets to maintain placement order!
						f.changexoff(celloffset)
			if event.type == KEYDOWN and (event.key == K_3 or event.key == K_KP3):
				if dispmode>2:
					celloffset=-(70*32)
					for f in celllist:
						#this IS CORRECT. upon initalization the cells store their origional offsets to maintain placement order!
						f.changexoff(celloffset)
			if event.type == KEYDOWN and (event.key == K_4 or event.key == K_KP4):
				if dispmode>2:
					celloffset=-(70*48)
					for f in celllist:
						#this IS CORRECT. upon initalization the cells store their origional offsets to maintain placement order!
						f.changexoff(celloffset)
				
				
			if event.type == QUIT:
				progactive=0
			if event.type==MOUSEBUTTONDOWN:
				if hudiconrect.collidepoint(event.pos):
					OKpop("Floored Square Simple Drum Loop "+versioninfo, copyrightinfo, "A 64-event, 5 tone drum sequencer.")
				if loadbx.collidepoint(event.pos):
					nameret=nameloader("Type or double click file to load:")
					if nameret!=None:
						rthmload(nameret)
						
				if savebx.collidepoint(event.pos):
					nameret=nameloader("Type or double click file to save to:")
					if nameret!=None and nameret:
						if not os.path.isfile(nameret):
							rthmsave(nameret)
						else:
							if YNpop("file: \"" + nameret + "\"exists. overwrite?"):
								rthmsave(nameret)
				#first attempt did not work. disabling for now.
				#if volup.collidepoint(event.pos):
					#mainvolume+=0.1
					#if mainvolume>1.0:
						#mainvolume=1.0
					#setvols()
				#if voldown.collidepoint(event.pos):
					#mainvolume-=0.1
					#if mainvolume<0.1:
						#mainvolume=0.1
					#setvols()
				if bpmup.collidepoint(event.pos):
					BPM+=5
					waittime=bpmdecode(BPM)
				if bpmdown.collidepoint(event.pos):
					BPM-=5
					if BPM<=0:
						BPM=5
					waittime=bpmdecode(BPM)
				if cpbup.collidepoint(event.pos):
					timefraction+=1
					waittime=bpmdecode(BPM)
				if cpbdown.collidepoint(event.pos):
					timefraction-=1
					if timefraction==0:
						timefraction=1
					waittime=bpmdecode(BPM)
				if scrollbar.collidepoint(event.pos) and event.button==4:
					celloffset+=70
					if celloffset>0:
						celloffset=0
					if dispmode==2:
						if celloffset<-(70*16):
							celloffset=-(70*16)
					elif dispmode==3:
						if celloffset<-(70*48):
							celloffset=-(70*48)
					else:
						celloffset=0
					for f in celllist:
						#this IS CORRECT. upon initalization the cells store their origional offsets to maintain placement order!
						f.changexoff(celloffset)
				if scrollbar.collidepoint(event.pos) and event.button==5:
					celloffset-=70
					if dispmode==2:
						if celloffset<-(70*16):
							celloffset=-(70*16)
					elif dispmode==3:
						if celloffset<-(70*48):
							celloffset=-(70*48)
					else:
						celloffset=0
					for f in celllist:
						#this IS CORRECT. upon initalization the cells store their origional offsets to maintain placement order!
						f.changexoff(celloffset)
				if displaymode.collidepoint(event.pos):
					if dispmode==0:
						dispmode=1
						screensurf=pygame.display.set_mode((1130, 550))
					elif dispmode==1:
						dispmode=2
						screensurf=pygame.display.set_mode((1130, 550))
					elif dispmode==2:
						dispmode=3
						screensurf=pygame.display.set_mode((1130, 550))
					elif dispmode==3:
						dispmode=0
						screensurf=pygame.display.set_mode((570, 550))
					else:
						dispmode=0
						screensurf=pygame.display.set_mode((570, 550))
					celloffset=0
					for f in celllist:
						#this IS CORRECT. upon initalization the cells store their origional offsets to maintain placement order!
						f.changexoff(celloffset)
				for cell in celllist:
					if cell.mainrect.collidepoint(event.pos):
						if event.button==3:
							gotocell=cell.cellid-1
						else:
							cell.clickevent(event.pos, event.button)
					

def OKpop(info, extra=None, extra2=None):
	global progactive
	bgrect=pygame.Rect(0, 50, 450, 200)
	bgrect.centerx=(screensurf.get_width()//2)
	pygame.draw.rect(screensurf, (0, 0, 0), bgrect)
	pygame.draw.rect(screensurf, (255, 255, 255), bgrect, 1)
	yoff=2
	yjump=20
	lineren=simplefont.render(info, True, (255, 255, 255), (30, 30, 30))
	screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+50))
	yoff+=yjump
	if extra!=None:
		lineren=simplefont.render(extra, True, (255, 255, 255), (30, 30, 30))
		screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+50))
		yoff+=yjump
	if extra2!=None:
		lineren=simplefont.render(extra2, True, (255, 255, 255), (30, 30, 30))
		screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+50))
		yoff+=yjump
	lineren=simplefont.render("Press any key or click to continue", True, (255, 255, 255), (30, 30, 30))
	screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+50))
	yoff+=yjump
	pygame.display.update()
	while True:
		time.sleep(0.1)
		for event in pygame.event.get():
			if event.type == QUIT:
				progactive=0
				return
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				progactive=0
				return
			if event.type == KEYDOWN:
				return
			if event.type==MOUSEBUTTONDOWN:
				return

def YNpop(info):
	bgrect=pygame.Rect(0, 50, 450, 200)
	bgrect.centerx=(screensurf.get_width()//2)
	pygame.draw.rect(screensurf, (0, 0, 0), bgrect)
	pygame.draw.rect(screensurf, (255, 255, 255), bgrect, 1)
	yoff=2
	yjump=20
	lineren=simplefont.render(info, True, (255, 255, 255), (30, 30, 30))
	screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+50))
	yoff+=yjump
	lineren=simplefont.render("(Y)es or (N)o?", True, (255, 255, 255), (30, 30, 30))
	screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+50))
	yoff+=yjump
	pygame.display.update()
	while True:
		time.sleep(0.1)
		for event in pygame.event.get():
			if event.type == QUIT:
				progactive=0
				return 0
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				progactive=0
				return 0
			if event.type == KEYDOWN and event.key == K_n:
				return 0
			if event.type == KEYDOWN and event.key == K_y:
				return 1

rthmfilename=None

dispmode=0
celloffset=0
mainvolume=0.1
def rthmsave(name):
	global rthmfilename
	rthmfilename=name
	rthmfile=open(name, "w")
	rthmfile.write(str(BPM) + "-" + str(mainvolume) + "-" + str(dispmode) + "\n")
	rthmfile.write(str(timefraction) + "\n")
	for cell in celllist:
		rthmfile.write(str(cell.drumid) + "-" + str(cell.active) + "-" + str(cell.fade) + "-" + str(cell.vol) + "-" + str(cell.ts) + "\n")
	rthmfile.write("#Generated By: simpledrum.py: Floored Square Drum Loop. \n#Part of Floored Square Simple Synth, A chiptune-esq synthesizer suite.\n#" + versioninfo)
	rthmfile.close()
	pygame.display.set_caption(name + " - Floored Square Simple Drum Loop", name + " - Floored Square Simple Drum Loop")
		
def rthmload(name):
	global rthmfilename
	rthmfilename=name
	global BPM
	global waittime
	global timefraction
	global celllist
	global mainvolume
	global celloffset
	global dispmode
	global screensurf
	for cell in celllist:
		cell.reset()
	if os.path.isfile(name):
		rthmfile=open(name, "r")
		linecnt=1
		cellcnt=0
		for linecon in rthmfile:
			if linecnt==1:
				linesplit=(linecon.replace("\n", "")).split("-")
				BPM=int(linesplit[0])
				dispmode=1
				if len(linesplit)==3:
					mainvolume=float(linesplit[1])
					dispmode=int(linesplit[2])
					
			elif linecnt==2:
				timefraction=int(linecon.replace("\n", ""))
				waittime=bpmdecode(BPM)
			else:
				curcell=celllist[cellcnt]
				linelist=(linecon.replace("\n", "")).split("-")
				curcell.drumid=int(linelist[0])
				curcell.active=int(linelist[1])
				if len(linelist)==2:
					if int(linelist[0])==3:
						curcell.fade=100
						curcell._setfade_()
						curcell.vol=0.5
						curcell._setvols_()
					else:
						curcell.fade=250
						curcell._setfade_()
						curcell.vol=1.0
						curcell._setvols_()
				else:
					curcell.fade=int(linelist[2])
					curcell._setfade_()
					curcell.vol=float(linelist[3])
					curcell._setvols_()
					curcell.ts=int(linelist[4])
					
				cellcnt+=1
				if cellcnt==64:
					break
			linecnt+=1
		#update screen mode after loading
		if dispmode==0:
			screensurf=pygame.display.set_mode((570, 550))
		else:
			screensurf=pygame.display.set_mode((1130, 550))
		celloffset=0
		for f in celllist:
			#this IS CORRECT. upon initalization the cells store their origional offsets to maintain placement order!
			f.changexoff(celloffset)
		pygame.display.set_caption(name + " - Floored Square Simple Drum Loop", name + " - Floored Square Simple Drum Loop")
	else:
		OKpop("ERROR: File: \"" + name + "\" Not found.")
				
			
def charremove(string, indexq):
	if indexq==0:
		return string
	else:
		return (string[:(indexq-1)] + string[(indexq):])
def charinsert(string, char, indexq):
	if indexq==0:
		return char + string
	else:
		return (string[:(indexq-1)] + char + string[(indexq-1):])

def nameloader(title):
	curoffset=0
	redraw=1
	textstring=""
	pathlist=sorted(os.listdir('.'), key=str.lower)
	while True:
		time.sleep(0.1)
		if redraw==1:
			redraw=0
			yoff=2
			yjump=20
			bgrect=pygame.Rect(0, 50, 300,400)
			bgrect.centerx=(screensurf.get_width()//2)
			pygame.draw.rect(screensurf, (0, 0, 0), bgrect)
			pygame.draw.rect(screensurf, (255, 255, 255), bgrect, 1)
			lineren=simplefont.render(title, True, (255, 255, 255), (30, 30, 30))
			screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+50))
			yoff+=yjump
			linedict={}
			for line in pathlist:
				if line.endswith('.rthm'):
					if line.split(".")[0]==textstring:
						lineren=simplefont.render(line, True, (0, 0, 0), (255, 255, 255))
					else:
						lineren=simplefont.render(line, True, (255, 255, 255), (0, 0, 0))
					bxrect=screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+50))
					yoff+=yjump
					linedict[line.split(".")[0]]=bxrect
			
			abttextB=simplefont.render(textstring+".rthm", True, (255, 255, 255), (40, 40, 40))
			screensurf.blit(abttextB, ((screensurf.get_width()//2)-(abttextB.get_width()//2), 400))
			pygame.display.update()
		for event in pygame.event.get():
			if event.type==MOUSEBUTTONDOWN:
				for rectbx in linedict:
					if linedict[rectbx].collidepoint(event.pos):
						if rectbx==textstring:
							return rectbx+".rthm"
						textstring=rectbx
						redraw=1
				if not bgrect.collidepoint(event.pos):
					return None
			if event.type == KEYDOWN and event.key == K_BACKSPACE:
				if len(textstring)!=0 and curoffset!=0:
					textstring=charremove(textstring, curoffset)
					curoffset -= 1
					redraw=1
				break
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				return None
			elif event.type == KEYDOWN and event.key == K_RETURN:
				if textstring!="":
					return textstring+ ".rthm"
				else:
					OKpop("\".rthm\" is not a valid name.")
					return None
			elif event.type == KEYDOWN and event.key != K_TAB:
				curoffset += 1
				textstring=charinsert(textstring, str(event.unicode), curoffset)
				redraw=1
				break
			
			
gotocell=None


sideproc=Thread(target = sideprocess, args = [])
sideproc.start()



		
		

oldcell=celllist[7]
while progactive==1:
	if playtones==1:
		loopiter=0
		#for cell in celllist:
		while loopiter<len(celllist):
			cell=celllist[loopiter]
			loopiter+=1
			if progactive==0:
				break
			#if encounter an inactive cell, break iteration. else, wait calcualted time.
			oldcell.play=0
			if dispmode==0 and cell.cellid>8:
				break
			if dispmode==1 and cell.cellid>16:
				break
			if gotocell!=None:
				loopiter=gotocell
				gotocell=None
				cell=celllist[loopiter]
			elif cell.drumprocess():
				if cell.cellid==1:
					time.sleep(waittime)
				break
			else:
				cell.play=1
				time.sleep(waittime)
				oldcell=cell
	else:
		time.sleep(waittime)