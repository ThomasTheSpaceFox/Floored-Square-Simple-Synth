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

windowicon=pygame.image.load("fscr32.png")
pygame.display.set_icon(windowicon)
screensurf=pygame.display.set_mode((800, 600))
print (pygame.display.list_modes()[0])
pygame.display.set_caption("Floored Square Chip-remin", "Floored Square Chip-remin")
pygame.font.init()

simplefont = pygame.font.SysFont(None, 22)
iconhud=pygame.image.load("fscr.png").convert()

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
pygame.mixer.set_num_channels(4)

basefreq=20

maxfreq=2000

slidechan=pygame.mixer.Channel(0)
freqjump=maxfreq/float(800)
voljump=1.0/float(600)

def foobsin(num):
	return (math.floor(math.sin(num)) * 4500)


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
label55=simplefont.render((str(55)+"Hz"), True, (0, 255, 255), (0, 0, 0))
label110=simplefont.render((str(110)+"Hz"), True, (0, 255, 255), (0, 0, 0))
label220=simplefont.render((str(220)+"Hz"), True, (0, 255, 255), (0, 0, 0))
label440=simplefont.render((str(440)+"Hz"), True, (0, 255, 255), (0, 0, 0))
label880=simplefont.render((str(880)+"Hz"), True, (0, 255, 255), (0, 0, 0))
label1760=simplefont.render((str(1760)+"Hz"), True, (0, 255, 255), (0, 0, 0))

tracelist=[(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]

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
		OKpop("Floored Square Chip-remin "+versioninfo, copyrightinfo, "A Theremin-like Chiptune Synthesizer")
		abouttrigger=0
	screensurf.fill((0, 0, 0))
	
	tracelist.insert(0, mpos)
	del tracelist[-1]
	pygame.draw.lines(screensurf, (255, 127, 127), 0, tracelist)
	hudiconrect=screensurf.blit(iconhud, (screensurf.get_width()-68, screensurf.get_height()-68))
	#frequency graph guides
	pygame.draw.line(screensurf, (0, 255, 255), (55/freqjump, 0), (55/freqjump, 600))
	pygame.draw.line(screensurf, (0, 255, 255), (110/freqjump, 0), (110/freqjump, 600))
	pygame.draw.line(screensurf, (0, 255, 255), (220/freqjump, 0), (220/freqjump, 600))
	pygame.draw.line(screensurf, (0, 255, 255), (440/freqjump, 0), (440/freqjump, 600))
	pygame.draw.line(screensurf, (0, 255, 255), (880/freqjump, 0), (880/freqjump, 600))
	pygame.draw.line(screensurf, (0, 255, 255), (1760/freqjump, 0), (1760/freqjump, 600))
	
	screensurf.blit(label55, (55/freqjump+1, 40))
	screensurf.blit(label110, (110/freqjump+1, 0))
	screensurf.blit(label220, (220/freqjump+1, 40))
	screensurf.blit(label440, (440/freqjump+1, 0))
	screensurf.blit(label880, (880/freqjump+1, 0))
	screensurf.blit(label1760, (1760/freqjump+1, 0))
	
	pygame.draw.line(screensurf, (255, 255, 0), (mposx, 0), (mposx, 600))
	pygame.draw.line(screensurf, (255, 255, 0), (0, mpos[1]), (800, mpos[1]))
	freqlabel=simplefont.render((str(freq)+"Hz"), True, (255, 255, 0), (0, 0, 0))
	screensurf.blit(freqlabel, (mpos[0]-20, mpos[1]-20))
	
	slidechan.set_volume(vol)
	pygame.display.update()
	#print(freq)
	if freq<basefreq:
		freq=basefreq
	if slidechan.get_queue()==None and (pygame.key.get_pressed()[K_SPACE] or pygame.mouse.get_pressed()[0]):
		notearray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int((synthfreq/freq)*6))])
		sample=pygame.mixer.Sound(notearray)
		slidechan.queue(sample)
	else:
		time.sleep(.005)
		