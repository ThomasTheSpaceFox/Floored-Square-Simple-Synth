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
pygame.display.set_caption("Floored Square Reverb Synth (unfinished)", "Floored Square Reverb Synth (unfinished)")
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
pygame.mixer.set_num_channels(48)
print ("mixer frequency:" + str(synthfreq))
#pygame.mixer.set_num_channels(6)
print ("number of channels: "+ str(pygame.mixer.get_num_channels()))

reverbtime=0.07
reverbtime=0.1
reverbdecay=0.5

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

tonevolume=0.2
tonevolume=0.6
class notevoice:
	def __init__(self, tone, trigkeys, voicenum=1):
		self.voicenum=voicenum
		self.tone=tone
		self.trigkeys=trigkeys
		self.vol=tonevolume
		#self.notearray=array.array('i', [ewchunk(foobsin(2.0 * pival * (self.tone) * t / synthfreq)) for t in xrange(0, STACKRANGE)])
		#self.notearray=fssynthlib.makesquare(self.tone)
		self.notearray=fssynthlib.makesaw(self.tone)
		self.sample=pygame.mixer.Sound(self.notearray)
		self.sample.set_volume(self.vol)
		vol2=self.vol*reverbdecay
		vol3=vol2*reverbdecay
		vol4=vol3*reverbdecay
		vol5=vol4*reverbdecay
		vol6=vol5*reverbdecay
		vol7=vol6*reverbdecay
		vol8=vol7*reverbdecay
		self.sampled1=pygame.mixer.Sound(self.notearray)
		self.sampled1.set_volume(vol2)
		self.sampled2=pygame.mixer.Sound(self.notearray)
		self.sampled2.set_volume(vol3)
		self.sampled3=pygame.mixer.Sound(self.notearray)
		self.sampled3.set_volume(vol4)
		self.sampled4=pygame.mixer.Sound(self.notearray)
		self.sampled4.set_volume(vol5)
		self.sampled5=pygame.mixer.Sound(self.notearray)
		self.sampled5.set_volume(vol6)
		self.sampled6=pygame.mixer.Sound(self.notearray)
		self.sampled6.set_volume(vol7)
		self.sampled7=pygame.mixer.Sound(self.notearray)
		self.sampled7.set_volume(vol8)
		
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
			
			red=abs(24*self.playflag)+(len(tonelist)-self.voicenum)*5
			blue=(24*self.playflag)+self.voicenum*5
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
		pygame.draw.rect(screensurf, (red, 0, blue), self.drawrect)
		pygame.draw.rect(screensurf, (self.linered, 40, self.lineblue), self.drawrect, 4)
		pygame.draw.rect(screensurf, (255, 255, 255), self.drawrect, 1)
		pygame.draw.rect(screensurf, (255, 255, 255), self.playdrawrect, 1)
	
	def play(self):
		self.sample.play(-1)
		time.sleep(reverbtime)
		self.playflag=1
		self.sampled1.play(-1)
		time.sleep(reverbtime)
		self.playflag=2
		self.sampled2.play(-1)
		time.sleep(reverbtime)
		self.playflag=3
		self.sampled3.play(-1)
		time.sleep(reverbtime)
		self.playflag=4
		self.sampled4.play(-1)
		time.sleep(reverbtime)
		self.playflag=5
		self.sampled5.play(-1)
		time.sleep(reverbtime)
		self.playflag=6
		self.sampled6.play(-1)
		time.sleep(reverbtime)
		self.playflag=6
		self.sampled7.play(-1)
		self.playflag=7
	def stop(self):
		self.sample.stop()
		time.sleep(reverbtime)
		self.playflag=6
		self.sampled1.stop()
		time.sleep(reverbtime)
		self.playflag=5
		self.sampled2.stop()
		time.sleep(reverbtime)
		self.playflag=4
		self.sampled3.stop()
		time.sleep(reverbtime)
		self.playflag=3
		self.sampled4.stop()
		time.sleep(reverbtime)
		self.playflag=2
		self.sampled5.stop()
		time.sleep(reverbtime)
		self.playflag=1
		self.sampled6.stop()
		time.sleep(reverbtime)
		self.playflag=0
		self.sampled7.stop()


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
				
	