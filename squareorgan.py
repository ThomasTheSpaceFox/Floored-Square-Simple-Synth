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
from threading import Thread
pygame.display.init()

windowicon=pygame.image.load("icon32.png")
pygame.display.set_icon(windowicon)
screensurf=pygame.display.set_mode((800, 600))
print (pygame.display.list_modes()[0])
caption="SquareOrgan (unfinished)"
pygame.display.set_caption(caption, caption)
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

araylimit=1

#pygame.mixer.init()
pygame.mixer.init(frequency=synthfreq , size=-16)
pygame.mixer.set_num_channels(96)
print ("mixer frequency:" + str(synthfreq))
#pygame.mixer.set_num_channels(6)
print ("number of channels: "+ str(pygame.mixer.get_num_channels()))



progrun=1
pival=math.pi

def limit(limit, num):
	if num>limit:
		return limit
	elif num<-limit:
		return -limit
	else:
		return num

def foobtan(num):
	return (math.floor(math.tan(num)) * 3500)

def foobcos(num):
	return (math.floor(math.cos(num)) * 3500)
#def foobtan(num):
#	
	#return math.floor(math.sin((math.e**(num/100)))) * 4500
	#return abs(math.e**((num)/1000))
def foobsin(num):
	return (math.floor(math.sin(num)) * 3500)
#def foobsin(num):
#	return (math.floor(math.sin(num)-math.cos(num*2)-math.cos(num)) * 4500)
sinetan=0
tonevolume=0.08
tonevolume=0.06

#stops
stoptan=1
stopsin=1
stopcos=1

class notevoice:
	def __init__(self, tone, trigkeys, voicenum=1):
		self.voicenum=voicenum
		self.tone=tone
		self.trigkeys=trigkeys
		self.vol1=tonevolume
		
		#fsin stop
		self.notearray2=array.array('f', [(foobsin(2.0 * pival * (self.tone*1.0) * t / synthfreq)) for t in xrange(0, int(STACKRANGE//self.tone*1.0))])
		self.notearray1=array.array('f', [(foobsin(2.0 * pival * (self.tone/2.0) * t / synthfreq)) for t in xrange(0, int(STACKRANGE//(self.tone/2.0)))])
		self.notearray3=array.array('f', [(foobsin(2.0 * pival * (self.tone*2.0) * t / synthfreq)) for t in xrange(0, int(STACKRANGE//(self.tone*2.0)))])
		
		self.sampled1=pygame.mixer.Sound(self.notearray1)
		self.sampled1.set_volume(self.vol1)
		self.sampled2=pygame.mixer.Sound(self.notearray2)
		self.sampled2.set_volume(self.vol1)
		self.sampled3=pygame.mixer.Sound(self.notearray3)
		self.sampled3.set_volume(self.vol1)
		
		#fcos stop
		self.cosarray2=array.array('f', [(foobcos(2.0 * pival * (self.tone*1.0) * t / synthfreq)) for t in xrange(0, int(STACKRANGE//self.tone*1.0))])
		self.cosarray1=array.array('f', [(foobcos(2.0 * pival * (self.tone/2.0) * t / synthfreq)) for t in xrange(0, int(STACKRANGE//(self.tone/2.0)))])
		self.cosarray3=array.array('f', [(foobcos(2.0 * pival * (self.tone*2.0) * t / synthfreq)) for t in xrange(0, int(STACKRANGE//(self.tone*2.0)))])
		
		self.cos1=pygame.mixer.Sound(self.cosarray1)
		self.cos1.set_volume(self.vol1)
		self.cos2=pygame.mixer.Sound(self.cosarray2)
		self.cos2.set_volume(self.vol1)
		self.cos3=pygame.mixer.Sound(self.cosarray3)
		self.cos3.set_volume(self.vol1)
		#ftan stop
		self.tanarray2=array.array('f', [(foobtan(2.0 * pival * (self.tone/2.0) * t / synthfreq)) for t in xrange(0, int(STACKRANGE//self.tone/2.0))])
		self.tanarray1=array.array('f', [(foobtan(2.0 * pival * (self.tone/4.0) * t / synthfreq)) for t in xrange(0, int(STACKRANGE//(self.tone/4.0)))])
		self.tanarray3=array.array('f', [(foobtan(2.0 * pival * (self.tone*1.0) * t / synthfreq)) for t in xrange(0, int(STACKRANGE//(self.tone*1.0)))])

		
		self.tan1=pygame.mixer.Sound(self.tanarray1)
		self.tan1.set_volume(self.vol1)
		self.tan2=pygame.mixer.Sound(self.tanarray2)
		self.tan2.set_volume(self.vol1)
		self.tan3=pygame.mixer.Sound(self.tanarray3)
		self.tan3.set_volume(self.vol1)
		
		
		self.playflag=0
		self.firstrender=1
	def keyup(self, event):
		if event.key in self.trigkeys:
			self.stop()
	def keydown(self, event):
		if event.key in self.trigkeys:
			self.play()
	def render(self, offset):
		return
	
	def play(self):
		if stopsin:
			self.sampled1.play(-1)
			self.sampled2.play(-1)
			self.sampled3.play(-1)
		if stoptan:
			self.tan1.play(-1)
			self.tan2.play(-1)
			self.tan3.play(-1)
		if stopcos:
			self.cos1.play(-1)
			self.cos2.play(-1)
			self.cos3.play(-1)

		
	def stop(self):
		self.sampled1.stop()
		self.sampled2.stop()
		self.sampled3.stop()
		self.tan1.stop()
		self.tan2.stop()
		self.tan3.stop()
		self.cos1.stop()
		self.cos2.stop()
		self.cos3.stop()



def gentones():
	global tonelist
	nv=notevoice
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
	
	tonenum=1
	for tone in tonelist:
		tone.voicenum=tonenum
		tonenum+=1
	print("tones generated.")
gentones()
print("ready")
clock=pygame.time.Clock()
#NEEDS WORK!
while progrun==1:
	#time.sleep(0.05)
	clock.tick(30)
	#pygame.event.pump()
	for event in pygame.event.get():
		if event.type==KEYDOWN:
			for tone in tonelist:
				tone.keydown(event)
		if event.type==KEYUP:
			for tone in tonelist:
				tone.keyup(event)
		if event.type==QUIT:
			progrun=0
			break
	offset=33
	for tone in tonelist:
		
		tone.render(offset)
		offset+=23
	pygame.display.update()
				
	