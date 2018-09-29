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
import fssynthlib
from fssynthlib import ewchunk
from threading import Thread
pygame.display.init()

windowicon=pygame.image.load("fschr32.png")
pygame.display.set_icon(windowicon)
screensurf=pygame.display.set_mode((800, 600))
print (pygame.display.list_modes()[0])
pygame.display.set_caption("Floored Square Chord-remin", "Floored Square Chord-remin")
pygame.font.init()

simplefont = pygame.font.SysFont(None, 22)
iconhud=pygame.image.load("fschr.png").convert()

#controls the frequency of the synthesizer logic and pygame mixer.
#lower frequencies are faster, but are lower quality.

versioninfo="v2.0"
copyrightinfo="Copyright (c) 2016-2018 Thomas Leathers and contributors"

synthfreq=22050
#synthfreq=16000
#synthfreq=11025
synthfreq=8000

synthfreqmain=synthfreq

STACKRANGE=int(synthfreqmain/1)
pival=math.pi

pygame.mixer.init(frequency=synthfreq , size=-16)
pygame.mixer.set_num_channels(34)

basefreq=20

maxfreq=2000



freqjump=maxfreq/float(800)
voljump=1.0/float(600)

def foobsin(num):
	return (math.floor(math.sin(num)) * 32765) + 15000


abouttrigger=0

progactive=1
def backprocess():
	global progactive
	global abouttrigger
	while progactive==1:
		time.sleep(0.1)
		if abouttrigger==0:
			for event in pygame.event.get():
				if abouttrigger==1:
					break
				if event.type == QUIT:
					progactive=0
				if event.type == KEYDOWN and event.key == K_ESCAPE:
						progactive=0
				if event.type == MOUSEBUTTONDOWN:
					if hudiconrect.collidepoint(event.pos):
						abouttrigger=1
						break
					
	
sideproc=Thread(target = backprocess, args = [])
sideproc.start()


class nv:
	def __init__(self, tone, trigkeys, voicenum=1):
		self.voicenum=voicenum
		self.tone=tone
		self.trigkeys=trigkeys
		self.vol=0.5
		self.tracelist=[(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
		self.drawtracex=0
		self.playflag=0
		self.firstrender=1
		self.tx=0
		self.ispressed=0
	def drawtrace(self, mpos):
		qx=mpos[0]+self.tone/6
		self.tracelist.insert(0, (qx, mpos[1]))
		del self.tracelist[-1]
		if self.drawtracex:
			pygame.draw.lines(screensurf, (255, 127, 127), 0, self.tracelist)
			
	def keypressed(self, pressed, octave, vol):
		self.channel.set_volume(vol)
		#if octave==-1:
		#	octave=0.5
		#if octave==0:
		#	octave=0.25
		if octave==0:
			octave=0.001
		tone=self.tone*octave
		self.ispressed=0
		for f in self.trigkeys:
			self.drawtracex=0
			if pressed[f]:
				if self.channel.get_queue()==None:
					self.channel.queue(pygame.mixer.Sound(array.array('i', [ewchunk(foobsin(2.0 * pival * tone * t / synthfreq)) for t in xrange(self.tx, self.tx+int((synthfreq/(220))*6))])))
					self.tx=t
					#print(self.tx)
					self.drawtracex=1
					
					return
				self.ispressed=1
		if not self.ispressed:
			self.tx=0
					
		return
	def setchan(self, channel):
		self.voicenum=channel
		self.channel=pygame.mixer.Channel(self.voicenum)
		self.channel.set_volume(self.vol)
			
	
	
def gentones():
	global tonelist
	print("initializing tone objects...")
	#tone list.
	tonelist=[nv(65, [K_z]),
	nv(69, [K_s]),
	nv(74, [K_x]),
	nv(78, [K_d]),
	nv(82, [K_c]),
	nv(87, [K_v]),
	nv(92, [K_g]),
	nv(98, [K_b]),
	nv(104, [K_h]),
	nv(110, [K_n]),
	nv(116, [K_j]),
	nv(123, [K_m]),
	nv(131, [K_q, K_LESS, K_COMMA]),
	nv(139, [K_2, K_l]),
	nv(147, [K_w, K_GREATER, K_PERIOD]),
	nv(156, [K_3, K_COLON, K_SEMICOLON]),
	nv(165, [K_e, K_SLASH, K_QUESTION]),
	nv(175, [K_r]),
	nv(185, [K_5]),
	nv(196, [K_t]),
	nv(208, [K_6]),
	nv(220, [K_y]),
	nv(233, [K_7]),
	nv(247, [K_u]),
	nv(262, [K_i]),
	nv(277, [K_9]),
	nv(294, [K_o]),
	nv(311, [K_0]),
	nv(330, [K_p]),
	nv(349, [K_LEFTBRACKET]),
	nv(370, [K_EQUALS, K_PLUS]),
	nv(392, [K_RIGHTBRACKET])]
	
	tonenum=0
	for tone in tonelist:
		tone.setchan(tonenum)
		tonenum+=1
	print("tones ready.")	



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

hudiconrect=None
labelquarter=simplefont.render((str(0.25)), True, (0, 255, 255), (0, 0, 0))
labelhalf=simplefont.render((str(0.5)), True, (0, 255, 255), (0, 0, 0))
labelm1=simplefont.render((str(1)), True, (255, 0, 255), (0, 0, 0))
labelm2=simplefont.render((str(2)), True, (255, 0, 255), (0, 0, 0))
labelm3=simplefont.render((str(3)), True, (255, 0, 255), (0, 0, 0))
labelm4=simplefont.render((str(4)), True, (255, 0, 255), (0, 0, 0))
labelm5=simplefont.render((str(5)), True, (255, 0, 255), (0, 0, 0))
labelm6=simplefont.render((str(6)), True, (255, 0, 255), (0, 0, 0))
gentones()
while progactive==1:
	mpos=pygame.mouse.get_pos()
	pygame.event.pump()
	mposx=mpos[0]
	freq=mposx*freqjump
	mposy=600-mpos[1]
	vol=mposy*voljump
	if vol<0.001:
		vol=0.001
	if abouttrigger==1:
		OKpop("Floored Square Chord-remin "+versioninfo, copyrightinfo, "A Theremin-like Chiptune Sliding Chord Synthesizer")
		abouttrigger=0
	screensurf.fill((0, 0, 0))
	
	#tracedraw
	#for f in tonelist:
	#	f.drawtrace(mpos)
	
	
	hudiconrect=screensurf.blit(iconhud, (screensurf.get_width()-68, screensurf.get_height()-68))
	popval=(800/5.0)
	pygame.draw.line(screensurf, (255, 0, 255), (popval*0.25, 0), (popval*0.25, 600))
	pygame.draw.line(screensurf, (255, 0, 255), (popval*0.5, 0), (popval*0.5, 600))
	pygame.draw.line(screensurf, (255, 0, 255), (popval*1, 0), (popval*1, 600))
	pygame.draw.line(screensurf, (255, 0, 255), (popval*2, 0), (popval*2, 600))
	pygame.draw.line(screensurf, (255, 0, 255), (popval*3, 0), (popval*3, 600))
	pygame.draw.line(screensurf, (255, 0, 255), (popval*4, 0), (popval*4, 600))
	pygame.draw.line(screensurf, (255, 0, 255), (popval*5, 0), (popval*5, 600))
	pygame.draw.line(screensurf, (255, 255, 0), (mposx, 0), (mposx, 600))
	pygame.draw.line(screensurf, (255, 255, 0), (0, mpos[1]), (800, mpos[1]))
	
	octave=(((mposx+1)/800.0)*5.0)
	freqlabel=simplefont.render((str(octave)+"(mul)"), True, (255, 255, 0), (0, 0, 0))
	screensurf.blit(freqlabel, (mpos[0]-20, mpos[1]-20))
	#print octave
	
	pygame.display.update()
	#print(freq)
	key=pygame.key.get_pressed()
	if freq<basefreq:
		freq=basefreq
	noevents=1
	for f in tonelist:
		f.keypressed(key, octave, vol)
	if noevents==1:
		time.sleep(.005)
		