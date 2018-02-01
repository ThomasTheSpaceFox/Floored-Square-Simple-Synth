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
screensurf=pygame.display.set_mode((570, 500))
print (pygame.display.list_modes()[0])
pygame.display.set_caption("Floored Square Simple Drum Loop", "Floored Square Simple Drum Loop")
pygame.font.init()

simplefont = pygame.font.SysFont(None, 22)
iconhud=pygame.image.load("fssdl.png").convert()

#controls the frequency of the synthesizer logic and pygame mixer.
#lower frequencies are faster, but are lower quality.

versioninfo="v2.8"
copyrightinfo="Copyright (c) 2016-2018 Thomas Leathers"

synthfreq=22050
#synthfreq=16000
#synthfreq=11025
#synthfreq=8000

synthfreqmain=synthfreq

STACKRANGE=int(synthfreqmain/1)
pival=math.pi

pygame.mixer.init(frequency=synthfreq , size=-16)
pygame.mixer.set_num_channels(24)

def foobsin(num):
	return (math.floor(math.sin(num)) * 4500)
	
class drum:
	def __init__(self, tone, fade):
		self.tone=tone
		self.notearray=array.array('f', [(foobsin(2.0 * pival * (self.tone) * t / synthfreq)) for t in xrange(0, STACKRANGE)])
		self.sample=pygame.mixer.Sound(self.notearray)
		self.fade=fade
	def play(self):
		self.sample.play(-1)
		self.sample.fadeout(self.fade)
		

class cymbal:
	def __init__(self, fade):
		self.notearray=array.array('f', [(random.uniform(-0.3, 0.3)) for t in xrange(0, STACKRANGE)])
		self.sample=pygame.mixer.Sound(self.notearray)
		self.sample.set_volume(0.5)
		self.fade=fade
	def play(self):
		self.sample.play(-1)
		self.sample.fadeout(self.fade)
bass=drum(55, 250)
#bass.play()
#time.sleep(0.3)
snare=drum(110, 250)
#snare.play()
#time.sleep(0.3)

cymbal=cymbal(100)
class beatcell:
	def __init__(self, xoff, drumid, cellid, active=1, yoff=20):
		self.mainrect=pygame.Rect(xoff, yoff, 60, 360)
		self.actlight=pygame.Rect(xoff+3, yoff+2, 54, 10)
		self.interrlight=pygame.Rect(xoff+3, yoff+14, 54, 40)
		self.drum0=pygame.Rect(xoff+3, yoff+60, 54, 55)
		self.drum1=pygame.Rect(xoff+3, yoff+120, 54, 55)
		self.drum2=pygame.Rect(xoff+3, yoff+180, 54, 55)
		self.drum3=pygame.Rect(xoff+3, yoff+240, 54, 55)
		self.play=0
		self.active=active
		self.drumid=drumid
		self.cellid=cellid
		self.xoff=xoff
		self.yoff=yoff
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
	def clickevent(self, pos):
		if self.interrlight.collidepoint(pos):
			if self.active==1:
				self.active=0
			else:
				self.active=1
		if self.drum0.collidepoint(pos):
			self.drumid=0
		if self.drum1.collidepoint(pos):
			self.drumid=1
		if self.drum2.collidepoint(pos):
			self.drumid=2
		if self.drum3.collidepoint(pos):
			self.drumid=3
		
		
	def render(self):
		pygame.draw.rect(screensurf, (30, 30, 30), self.mainrect)
		screensurf.blit(self.label1, (self.xoff, self.yoff+310))
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
	def drumprocess(self):
		if self.active==0:
			return 1
		else:
			if self.drumid==1:
				bass.play()
			elif self.drumid==2:
				snare.play()
			elif self.drumid==3:
				cymbal.play()
			return 0




playtones=1
pygame.display.update()

celllist=[]
xoff=10
for cell in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]:
	celllist.extend([beatcell(xoff, 0, cell, 0)])
	xoff+=70

timefraction=4

def bpmdecode(beatspermin):
	return (60.0/beatspermin/timefraction)
BPM=120
waittime=bpmdecode(BPM)
progactive=1
bpmup=pygame.Rect(2, 390, 60, 40)
displaymode=pygame.Rect(90, 390, 90, 40)
bpmdown=pygame.Rect(2, 460, 60, 40)
cpbup=pygame.Rect(190, 390, 60, 40)
cpbdown=pygame.Rect(190, 460, 60, 40)

loadbx=pygame.Rect(280, 460, 70, 40)
savebx=pygame.Rect(280, 390, 70, 40)

cpbuplabel=simplefont.render("CPB +1", True, (255, 255, 255), (30, 30, 160))
cpbdownlabel=simplefont.render("CPB -1", True, (255, 255, 255), (30, 30, 160))

loadlabel=simplefont.render("Load(F3)", True, (255, 255, 255), (30, 30, 160))
savelabel=simplefont.render("Save(F2)", True, (255, 255, 255), (30, 30, 160))

bpmuplabel=simplefont.render("BPM +5", True, (255, 255, 255), (30, 30, 160))

bpmdownlabel=simplefont.render("BPM -5", True, (255, 255, 255), (30, 30, 160))
dispmode=0
dispm0=simplefont.render("use 8 cells", True, (255, 255, 255), (30, 30, 160))
dispm1=simplefont.render("use 16 cells", True, (255, 255, 255), (30, 30, 160))
def sideprocess():
	global BPM
	global waittime
	global progactive
	global screensurf
	global dispmode
	global timefraction
	print("starting event handler thread...")
	while progactive==1:
		screensurf.fill((60, 60, 60))
		hudiconrect=screensurf.blit(iconhud, (screensurf.get_width()-68, screensurf.get_height()-68))
		time.sleep(0.05)
		#call render routines of cells
		for cell in celllist:
			cell.render()
		#box drawing
		pygame.draw.rect(screensurf, (30, 30, 160), bpmup)
		pygame.draw.rect(screensurf, (30, 30, 160), bpmdown)
		pygame.draw.rect(screensurf, (30, 30, 160), cpbup)
		pygame.draw.rect(screensurf, (30, 30, 160), cpbdown)
		pygame.draw.rect(screensurf, (30, 30, 160), displaymode)
		pygame.draw.rect(screensurf, (30, 30, 160), loadbx)
		pygame.draw.rect(screensurf, (30, 30, 160), savebx)
		#labels
		bpmlabel=simplefont.render(str(BPM), True, (255, 255, 255), (60, 60, 60))
		cpblabel=simplefont.render("Cells/Beat "+str(timefraction), True, (255, 255, 255), (60, 60, 60))
		screensurf.blit(bpmuplabel, (bpmup.x+2, bpmup.y+2))
		screensurf.blit(bpmdownlabel, (bpmdown.x+2, bpmdown.y+2))
		screensurf.blit(bpmlabel, (bpmup.x+2, bpmup.y+42))
		screensurf.blit(cpbuplabel, (cpbup.x+2, cpbup.y+2))
		screensurf.blit(cpbdownlabel, (cpbdown.x+2, cpbdown.y+2))
		screensurf.blit(cpblabel, (cpbup.x+2, cpbup.y+42))
		screensurf.blit(loadlabel, (loadbx.x+2, loadbx.y+2))
		screensurf.blit(savelabel, (savebx.x+2, savebx.y+2))
		
		if dispmode==1:
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
			if event.type == QUIT:
				progactive=0
			if event.type==MOUSEBUTTONDOWN:
				if hudiconrect.collidepoint(event.pos):
					OKpop("Floored Square Simple Drum Loop "+versioninfo, copyrightinfo)
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
				if displaymode.collidepoint(event.pos):
					if dispmode==0:
						dispmode=1
						screensurf=pygame.display.set_mode((1130, 500))
					else:
						dispmode=0
						screensurf=pygame.display.set_mode((570, 500))
				for cell in celllist:
					if cell.mainrect.collidepoint(event.pos):
						cell.clickevent(event.pos)
					

def OKpop(info, extra=None):
	bgrect=pygame.Rect(0, 50, 300, 200)
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
	lineren=simplefont.render("Press any key or click to continue", True, (255, 255, 255), (30, 30, 30))
	screensurf.blit(lineren, ((screensurf.get_width()//2)-(lineren.get_width()//2), yoff+50))
	yoff+=yjump
	pygame.display.update()
	while True:
		time.sleep(0.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				return
			if event.type==MOUSEBUTTONDOWN:
				return

def YNpop(info):
	bgrect=pygame.Rect(0, 50, 300, 200)
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
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				return 0
			if event.type == KEYDOWN and event.key == K_n:
				return 0
			if event.type == KEYDOWN and event.key == K_y:
				return 1
	

def rthmsave(name):
	rthmfile=open(name, "w")
	rthmfile.write(str(BPM) + "\n")
	rthmfile.write(str(timefraction) + "\n")
	for cell in celllist:
		rthmfile.write(str(cell.drumid) + "-" + str(cell.active) + "\n")
	rthmfile.close()
		
def rthmload(name):
	global BPM
	global waittime
	global timefraction
	global celllist
	if os.path.isfile(name):
		rthmfile=open(name, "r")
		linecnt=1
		cellcnt=0
		for linecon in rthmfile:
			if linecnt==1:
				BPM=int(linecon.replace("\n", ""))
			elif linecnt==2:
				timefraction=int(linecon.replace("\n", ""))
				waittime=bpmdecode(BPM)
			else:
				curcell=celllist[cellcnt]
				linelist=(linecon.replace("\n", "")).split("-")
				curcell.drumid=int(linelist[0])
				curcell.active=int(linelist[1])
				cellcnt+=1
			linecnt+=1
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
			
			
	


sideproc=Thread(target = sideprocess, args = [])
sideproc.start()



		
		

oldcell=celllist[7]
while progactive==1:
	if playtones==1:
		for cell in celllist:
			#if encounter an inactive cell, break iteration. else, wait calcualted time.
			oldcell.play=0
			if dispmode==0 and cell.cellid>8:
				break
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