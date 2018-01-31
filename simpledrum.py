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

windowicon=pygame.image.load("icon32.png")
pygame.display.set_icon(windowicon)
screensurf=pygame.display.set_mode((570, 500))
print (pygame.display.list_modes()[0])
pygame.display.set_caption("Floored Square Simple Drum Loop", "Floored Square Simple Drum Loop")
pygame.font.init()

simplefont = pygame.font.SysFont(None, 22)
bgimg=pygame.image.load("simplesynth.jpg").convert()

#controls the frequency of the synthesizer logic and pygame mixer.
#lower frequencies are faster, but are lower quality.

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
	
	if cell>=3:
		celllist.extend([beatcell(xoff, 0, cell, 0)])
	elif cell>1:
		celllist.extend([beatcell(xoff, 1, cell)])
	else:
		celllist.extend([beatcell(xoff, 2, cell)])
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

cpbuplabel=simplefont.render("CPB +1", True, (255, 255, 255), (30, 30, 160))
cpbdownlabel=simplefont.render("CPB -1", True, (255, 255, 255), (30, 30, 160))

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
		time.sleep(0.05)
		for cell in celllist:
			cell.render()
		pygame.draw.rect(screensurf, (30, 30, 160), bpmup)
		pygame.draw.rect(screensurf, (30, 30, 160), bpmdown)
		pygame.draw.rect(screensurf, (30, 30, 160), cpbup)
		pygame.draw.rect(screensurf, (30, 30, 160), cpbdown)
		pygame.draw.rect(screensurf, (30, 30, 160), displaymode)
		bpmlabel=simplefont.render(str(BPM), True, (255, 255, 255), (60, 60, 60))
		cpblabel=simplefont.render("Cells/Beat "+str(timefraction), True, (255, 255, 255), (60, 60, 60))
		screensurf.blit(bpmuplabel, (bpmup.x+2, bpmup.y+2))
		screensurf.blit(bpmdownlabel, (bpmdown.x+2, bpmdown.y+2))
		screensurf.blit(bpmlabel, (bpmup.x+2, bpmup.y+42))
		screensurf.blit(cpbuplabel, (cpbup.x+2, cpbup.y+2))
		screensurf.blit(cpbdownlabel, (cpbdown.x+2, cpbdown.y+2))
		screensurf.blit(cpblabel, (cpbup.x+2, cpbup.y+42))
		if dispmode==1:
			screensurf.blit(dispm0, (displaymode.x+2, displaymode.y+2))
		else:
			screensurf.blit(dispm1, (displaymode.x+2, displaymode.y+2))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				progactive=0
			if event.type == QUIT:
				progactive=0
			if event.type==MOUSEBUTTONDOWN:
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
				break
			else:
				cell.play=1
				time.sleep(waittime)
				oldcell=cell
	else:
		time.sleep(waittime)