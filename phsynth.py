#!/usr/bin/env python
import pygame.event
import pygame.key
import pygame.display
import pygame.image
import pygame.mixer
import pygame
from fssynthlib import ewchunk
import fssynthlib
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
pygame.display.set_caption("Floored Square Phase Synth (unfinished)", "Floored Square Phase Synth (unfinished)")
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
pygame.mixer.set_num_channels(64)
print ("mixer frequency:" + str(synthfreq))
#pygame.mixer.set_num_channels(6)
print ("number of channels: "+ str(pygame.mixer.get_num_channels()))

reverbtimein=0.07
reverbtimeout=0.07
reverbdecay=0.5
fadeouttime=10
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
	return (math.floor(math.tan(num)) * 4500)
#def foobtan(num):
#	
	#return math.floor(math.sin((math.e**(num/100)))) * 4500
	#return abs(math.e**((num)/1000))
def foobsin(num):
	return (math.floor(math.sin(num)) * 32000)



#def foobsin(num):
#	return (math.floor(math.sin(num)-math.cos(num*2)-math.cos(num)) * 4500)
shift=0.01
tonevolume=0.2
tonevolume=0.6
class notevoice:
	def __init__(self, tone, trigkeys, voicenum=1):
		self.voicenum=voicenum
		self.tone=tone
		self.Rtone=tone
		self.Ltone=tone
		self.vol=tonevolume
		self.channelL=pygame.mixer.Channel(voicenum)
		self.channelR=pygame.mixer.Channel(voicenum+32)
		
		while self.Ltone==self.Rtone:
			self.Ltone=tone*(1.0+shift)
			self.Rtone=tone*(1.0-shift)
		self.trigkeys=trigkeys
		
		self.notearrayL=fssynthlib.maketri(self.Ltone)
		self.sampleL=pygame.mixer.Sound(self.notearrayL)
		#self.sampleL.set_volume(self.vol)
		self.notearrayR=fssynthlib.maketri(self.Rtone)
		self.sampleR=pygame.mixer.Sound(self.notearrayR)
		#self.sampleR.set_volume(self.vol)
		self.playflag=0
		self.firstrender=1
	def keyup(self, event):
		if event.key in self.trigkeys:
			sideproc=Thread(target = self.stop, args = [])
			sideproc.start()
	def keydown(self, event):
		if event.key in self.trigkeys:
			sideproc=Thread(target = self.play, args = [])
			sideproc.start()	
		return 0
	def render(self, offset):
		if self.firstrender==1:
			self.firstrender=0
			self.linered=abs(24*3)+(len(tonelist)-self.voicenum)*5
			self.lineblue=(24*3)+self.voicenum*5
			self.drawrect=Rect(offset, 10, 20, 130+(3*(len(tonelist)-self.voicenum)))
		#linered2=abs(24*1)+(len(tonelist)-self.voicenum)*5
		#lineblue2=(24*1)+self.voicenum*5
		if self.playflag!=0:
			
			red=abs(24*self.playflag*2)+(len(tonelist)-self.voicenum)*5
			blue=(24*self.playflag*2)+self.voicenum*5
			lenset=((130+(3*(len(tonelist)-self.voicenum)))//7)*self.playflag
			#print(self.voicenum)
			#print(red)
			#print(blue)
			#submod=254//len(tonelist)//(7-self.playflag)
			#red=0+((len(tonelist)-self.voicenum)*submod)
			#blue=0+(self.voicenum*submod)
			if red>255:
				red=255
			if blue>255:
				blue=255
			#print(red)
			#print(blue)
		else:
			red=0
			blue=0
			lenset=1
		self.playdrawrect=Rect(offset, 10, 20, lenset)
		pygame.draw.rect(screensurf, (0, red, blue), self.drawrect)
		pygame.draw.rect(screensurf, (40, self.linered, self.lineblue), self.drawrect, 4)
		pygame.draw.rect(screensurf, (255, 255, 255), self.drawrect, 1)
		#pygame.draw.rect(screensurf, (255, 255, 255), self.playdrawrect, 1)
	
	def play(self):
		self.playflag=1
		self.channelL.stop()
		self.channelR.stop()
		self.channelL.set_volume(self.vol, 0)
		self.channelR.set_volume(0, self.vol)
		self.channelL.play(self.sampleL, -1)
		self.channelR.play(self.sampleR, -1)
	def stop(self):
		self.playflag=0
		self.channelL.fadeout(fadeouttime)
		self.channelR.fadeout(fadeouttime)
		


def gentones():
	global tonelist
	nv=notevoice
	print("initializing tone objects...")
	#tone list.
	tonelist=[nv(65, [K_z], 0),
	nv(69, [K_s], 1),
	nv(74, [K_x], 2),
	nv(78, [K_d], 3),
	nv(82, [K_c], 4),
	nv(87, [K_v], 5),
	nv(92, [K_g], 6),
	nv(98, [K_b], 7),
	nv(104, [K_h], 8),
	nv(110, [K_n], 9),
	nv(116, [K_j], 10),
	nv(123, [K_m], 11),
	nv(131, [K_q, K_LESS, K_COMMA], 12),
	nv(139, [K_2, K_l], 13),
	nv(147, [K_w, K_GREATER, K_PERIOD], 14),
	nv(156, [K_3, K_COLON, K_SEMICOLON], 15),
	nv(165, [K_e, K_SLASH, K_QUESTION], 16),
	nv(175, [K_r], 17),
	nv(185, [K_5], 18),
	nv(196, [K_t], 19),
	nv(208, [K_6], 20),
	nv(220, [K_y], 21),
	nv(233, [K_7], 22),
	nv(247, [K_u], 23),
	nv(262, [K_i], 24),
	nv(277, [K_9], 25),
	nv(294, [K_o], 26),
	nv(311, [K_0], 27),
	nv(330, [K_p], 28),
	nv(349, [K_LEFTBRACKET], 29),
	nv(370, [K_EQUALS, K_PLUS], 30),
	nv(392, [K_RIGHTBRACKET], 31)]
	
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
				
	