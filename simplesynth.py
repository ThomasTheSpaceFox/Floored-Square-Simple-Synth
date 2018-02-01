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
pygame.display.set_caption("Floored Square Simple Synth", "Floored Square Simple Synth")
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
pygame.mixer.set_num_channels(24)
print ("mixer frequency:" + str(synthfreq))
#pygame.mixer.set_num_channels(6)
print ("number of channels: "+ str(pygame.mixer.get_num_channels()))
def foobsin1(num):
	return (strex(math.sin(num)) * 4500)
def foobsin2(num):
	return (strex(math.tan(num)) * 4500)
def foobsin3(num):
	return (strex(math.cos(num) + math.sin(num)) * 4500)	
def foobsin4(num):
	return (strex(math.tan(num) + math.sin(num)) * 4500)
foobsin=foobsin1

def vstroke(num):
	if num<0.5:
		return math.ceil(num)
	else:
		return math.floor(num)
def jstroke(num):
	if num>0.5:
		return math.ceil(abs(num) - abs(num) - abs(num))
	else:
		return math.floor(abs(num))
def cstroke(num):
	if num>0.5:
		return math.floor(abs(num) - abs(num) - abs(num))
	else:
		return math.floor(abs(num))
def wstroke(num):
	if num>0.7:
		return math.ceil(num)
	elif num<0.3:
		return math.floor(num)
	else:
		return float(0.5)
def wstroke(num):
	if num>0.5:
		return math.ceil(num)
	elif num<(-0.5):
		return math.floor(num)
	else:
		return float(0.0)
def three_way(num):
	if num>0.5:
		return float(0.9)
	elif num<(-0.5):
		return float(-0.9)
	else:
		return float(0.0)
def two_way(num):
	if num>=0:
		return float(1)
	else:
		return float(0)
strex=math.floor
#strex=two_way
#def dummyfunct(arg):
#	return arg
strexmd=1
wavemode=1

retrigtime=0.1


stackit=1
octshift=1
stackmod=1
def autosquare(freq, lenth):
	global STACKRANGE
	if octshift==0:
		freq=(freq/2.0)
	elif octshift==-1:
		freq=(freq/3.0)
	else:
		freq=(freq*octshift)
	#print freq
	#STACKRANGE=(1)*int((synthfreqmain / araylimit) // (freq / float(stacksub)))
	STACKRANGE=(1)*int((synthfreqmain / araylimit) / (freq /float((stackit) / (stacksub))))
	#print stackmod
	if stackmod==1:
		if stackit==1:
			retarray=autosquare1stack(freq, lenth)
		elif stackit==2:
			retarray=autosquare2stack(freq, lenth)
		elif stackit==3:
			retarray=autosquare3stack(freq, lenth)
		elif stackit==4:
			retarray=autosquare4stack(freq, lenth)
		elif stackit==5:
			retarray=autosquare5stack(freq, lenth)
		else:
			retarray=autosquare1stack(freq, lenth)
	elif stackmod==3:
		if stackit==1:
			retarray=autosquare1stack(freq, lenth)
		elif stackit==2:
			retarray=autosquare2stackne(freq, lenth)
		elif stackit==3:
			retarray=autosquare3stacknexq(freq, lenth)
		elif stackit==4:
			retarray=autosquare4stacknexq(freq, lenth)
		elif stackit==5:
			retarray=autosquare5stacknexq(freq, lenth)
		else:
			retarray=autosquare1stack(freq, lenth)
	elif stackmod==4:
		if stackit==1:
			retarray=autosquare1stack(freq, lenth)
		elif stackit==2:
			retarray=autosquare2stack(freq, lenth)
		elif stackit==3:
			retarray=autosquare3stackaddmean(freq, lenth)
		elif stackit==4:
			retarray=autosquare4stackaddmean(freq, lenth)
		elif stackit==5:
			retarray=autosquare5stackaddmean(freq, lenth)
		else:
			retarray=autosquare1stack(freq, lenth)
	elif stackmod==5:
		if stackit==1:
			retarray=autosquare1stack(freq, lenth)
		elif stackit==2:
			retarray=autosquare2stackne(freq, lenth)
		elif stackit==3:
			retarray=autosquare3stacksubmean(freq, lenth)
		elif stackit==4:
			retarray=autosquare4stacksubmean(freq, lenth)
		elif stackit==5:
			retarray=autosquare5stacksubmean(freq, lenth)
		else:
			retarray=autosquare1stack(freq, lenth)
	elif stackmod==6:
		if stackit==1:
			retarray=autosquare1stack(freq, lenth)
		elif stackit==2:
			retarray=autosquare2stackmean(freq, lenth)
		elif stackit==3:
			retarray=autosquare3stackmean(freq, lenth)
		elif stackit==4:
			retarray=autosquare4stackmean(freq, lenth)
		elif stackit==5:
			retarray=autosquare5stackmean(freq, lenth)
		else:
			retarray=autosquare1stack(freq, lenth)
	else:
		if stackit==1:
			retarray=autosquare1stack(freq, lenth)
		elif stackit==2:
			retarray=autosquare2stackne(freq, lenth)
		elif stackit==3:
			retarray=autosquare3stackne(freq, lenth)
		elif stackit==4:
			retarray=autosquare4stackne(freq, lenth)
		elif stackit==5:
			retarray=autosquare5stackne(freq, lenth)
		else:
			retarray=autosquare1stack(freq, lenth)
	#return ( + retarray)
	#return arrayduplicate(retarray)
	#sys.exit()
	return retarray



pival=math.pi

stacksub=1

#add
def autosquare1stack(freq, lenth):
	temparray=array.array('f', [(foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq)) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare1stack(freq, lenth):
	temparray=array.array('f', [(foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq)) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare2stack(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) + foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare3stack(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) + foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq) + foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare4stack(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) + foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq) + foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq) + foobsin(2.0 * pival * (freq *(stacksub * 4)) * t / synthfreq))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray
	
def autosquare5stack(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) + foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq) + foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq) + foobsin(2.0 * pival * (freq *(stacksub * 4)) * t / synthfreq) + foobsin(2.0 * pival * (freq *(stacksub * 5)) * t / synthfreq))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray
#subtract
def autosquare2stackne(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) - foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare3stackne(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) - foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq) - foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare4stackne(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) - foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq) - foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq) - foobsin(2.0 * pival * (freq *(stacksub * 4)) * t / synthfreq))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare5stackne(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) - foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq) - foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq) - foobsin(2.0 * pival * (freq *(stacksub * 4)) * t / synthfreq) - foobsin(2.0 * pival * (freq *(stacksub * 5)) * t / synthfreq))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray
#adsub1
def autosquare2stacknexq(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) - (foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq)))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare3stacknexq(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) - (foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq) + foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq)))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare4stacknexq(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) - (foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq) + foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq) - foobsin(2.0 * pival * (freq *(stacksub * 4)) * t / synthfreq)))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare5stacknexq(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) - (foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq) + foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq) - foobsin(2.0 * pival * (freq *(stacksub * 4)) * t / synthfreq) + foobsin(2.0 * pival * (freq *(stacksub * 5)) * t / synthfreq)))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

#SUB ABS

def autosquare3stackaddmean(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) + mean([foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq)]))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare4stackaddmean(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) + mean([foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 4)) * t / synthfreq)]))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare5stackaddmean(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) + mean([foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 4)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 5)) * t / synthfreq)]))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

	
#sub mean

def autosquare3stacksubmean(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) - mean([foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq)]))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare4stacksubmean(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) - mean([foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 4)) * t / synthfreq)]))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare5stacksubmean(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq) - mean([foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 4)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 5)) * t / synthfreq)]))) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

#mean
def autosquare2stackmean(freq, lenth):
	temparray=array.array('f', [(mean([foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq)])) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare3stackmean(freq, lenth):
	temparray=array.array('f', [(mean([foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq)])) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare4stackmean(freq, lenth):
	temparray=array.array('f', [(mean([foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 4)) * t / synthfreq)])) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray

def autosquare5stackmean(freq, lenth):
	temparray=array.array('f', [(mean([foobsin(2.0 * pival * (freq * stacksub) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 2)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 3)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 4)) * t / synthfreq), foobsin(2.0 * pival * (freq *(stacksub * 5)) * t / synthfreq)])) for t in xrange(0, STACKRANGE)])
	#temparray=array.array('f', [(foobsin(2.0 * pival * freq * t / synthfreq)) for t in xrange(0, int(lenth * synthfreq))])
	return temparray



fadex=600
fadetime=fadex
notetime=(0.1)

def keycheckoff():
	keypressed=pygame.key.get_pressed()
	if fadetime!=0:
		if not keypressed[K_z]:
			snf0.fadeout(fadetime)
		if not keypressed[K_s]:
			snf1.fadeout(fadetime)
		if not keypressed[K_x]:
			snf2.fadeout(fadetime)
		if not keypressed[K_d]:
			snf3.fadeout(fadetime)
		if not keypressed[K_c]:
			snf4.fadeout(fadetime)
		if not keypressed[K_v]:
			snf5.fadeout(fadetime)
		if not keypressed[K_g]:
			snf5b.fadeout(fadetime)
		if not keypressed[K_b]:
			snf6.fadeout(fadetime)
		if not keypressed[K_h]:
			snf7.fadeout(fadetime)
		if not keypressed[K_n]:
			snf8.fadeout(fadetime)
		if not keypressed[K_j]:
			snf9.fadeout(fadetime)
		if not keypressed[K_m]:
			snf10.fadeout(fadetime)
		if not (keypressed[K_q] or keypressed[K_LESS] or keypressed[K_COMMA]):
			snf11.fadeout(fadetime)
		if not (keypressed[K_2] or keypressed[K_l]):
			snf12.fadeout(fadetime)
		if not (keypressed[K_w] or keypressed[K_GREATER] or keypressed[K_PERIOD]):
			snf13.fadeout(fadetime)
		if not (keypressed[K_3] or keypressed[K_COLON] or keypressed[K_SEMICOLON]):
			snf14.fadeout(fadetime)
		if not (keypressed[K_e] or keypressed[K_SLASH] or keypressed[K_QUESTION]):
			snf15.fadeout(fadetime)
		if not keypressed[K_r]:
			snf16.fadeout(fadetime)
		if not keypressed[K_5]:
			snf17.fadeout(fadetime)
		if not keypressed[K_t]:
			snf18.fadeout(fadetime)
		if not keypressed[K_6]:
			snf19.fadeout(fadetime)
		if not keypressed[K_y]:
			snf.fadeout(fadetime)
		if not keypressed[K_7]:
			snf20.fadeout(fadetime)
		if not keypressed[K_u]:
			snf21.fadeout(fadetime)
		if not keypressed[K_i]:
			snf22.fadeout(fadetime)
		if not keypressed[K_9]:
			snf23.fadeout(fadetime)
		if not keypressed[K_o]:
			snf24.fadeout(fadetime)
		if not keypressed[K_0]:
			snf25.fadeout(fadetime)
		if not keypressed[K_p]:
			snf26.fadeout(fadetime)
		if not keypressed[K_LEFTBRACKET]:
			snf27.fadeout(fadetime)
		if not (keypressed[K_EQUALS] or keypressed[K_PLUS]):
			snf28.fadeout(fadetime)
		if not keypressed[K_RIGHTBRACKET]:
			snf29.fadeout(fadetime)
	else:
		if not keypressed[K_z]:
			snf0.stop()
		if not keypressed[K_s]:
			snf1.stop()
		if not keypressed[K_x]:
			snf2.stop()
		if not keypressed[K_d]:
			snf3.stop()
		if not keypressed[K_c]:
			snf4.stop()
		if not keypressed[K_v]:
			snf5.stop()
		if not keypressed[K_g]:
			snf5b.stop()
		if not keypressed[K_b]:
			snf6.stop()
		if not keypressed[K_h]:
			snf7.stop()
		if not keypressed[K_n]:
			snf8.stop()
		if not keypressed[K_j]:
			snf9.stop()
		if not keypressed[K_m]:
			snf10.stop()
		if not (keypressed[K_q] or keypressed[K_LESS] or keypressed[K_COMMA]):
			snf11.stop()
		if not (keypressed[K_2] or keypressed[K_l]):
			snf12.stop()
		if not (keypressed[K_w] or keypressed[K_GREATER] or keypressed[K_PERIOD]):
			snf13.stop()
		if not (keypressed[K_3] or keypressed[K_COLON] or keypressed[K_SEMICOLON]):
			snf14.stop()
		if not (keypressed[K_e] or keypressed[K_SLASH] or keypressed[K_QUESTION]):
			snf15.stop()
		if not (keypressed[K_r]):
			snf16.stop()
		if not (keypressed[K_5]):
			snf17.stop()
		if not (keypressed[K_t]):
			snf18.stop()
		if not (keypressed[K_6]):
			snf19.stop()
		if not (keypressed[K_y]):
			snf.stop()
		if not (keypressed[K_7]):
			snf20.stop()
		if not (keypressed[K_u]):
			snf21.stop()
		if not (keypressed[K_i]):
			snf22.stop()
		if not (keypressed[K_9]):
			snf23.stop()
		if not (keypressed[K_o]):
			snf24.stop()
		if not (keypressed[K_0]):
			snf25.stop()
		if not (keypressed[K_p]):
			snf26.stop()
		if not keypressed[K_LEFTBRACKET]:
			snf27.stop()
		if not (keypressed[K_EQUALS] or keypressed[K_PLUS]):
			snf28.stop()
		if not keypressed[K_RIGHTBRACKET]:
			snf29.stop()


pleasewaittx=simplefont.render("Please wait... Generating samples...     ", True, (0, 0, 0), (255, 127, 127))
perc0tx=simplefont.render("0%", True, (0, 0, 0), (255, 127, 127))
perc25tx=simplefont.render("25%", True, (0, 0, 0), (255, 127, 127))
perc50tx=simplefont.render("50%", True, (0, 0, 0), (255, 127, 127))
perc75tx=simplefont.render("75%", True, (0, 0, 0), (255, 127, 127))
perc12tx=simplefont.render("12%", True, (0, 0, 0), (255, 127, 127))
perc37tx=simplefont.render("37%", True, (0, 0, 0), (255, 127, 127))
perc62tx=simplefont.render("62%", True, (0, 0, 0), (255, 127, 127))
perc87tx=simplefont.render("87%", True, (0, 0, 0), (255, 127, 127))
#Define sounds
def redefsounds():
	global WAVDRAW
	WAVDRAW=autosquare(110, notetime)
	dispupdate()
	screensurf.blit(pleasewaittx, (200, 580))
	screensurf.blit(perc0tx, (460, 580))
	pygame.display.update()
	global snf
	global snf0
	global snf1
	global snf2
	global snf3
	global snf4
	global snf5
	global snf5b
	global snf6
	global snf7
	global snf8
	global snf9
	global snf10
	global snf11
	global snf12
	global snf13
	global snf14
	global snf15
	global snf16
	global snf17
	global snf18
	global snf19
	global snf20
	global snf21
	global snf22
	global snf23
	global snf24
	global snf25
	global snf26
	global snf27
	global snf28
	global snf29
	
	snf0=pygame.mixer.Sound(autosquare(65, notetime))
	snf1=pygame.mixer.Sound(autosquare(69, notetime))
	snf2=pygame.mixer.Sound(autosquare(74, notetime))
	snf3=pygame.mixer.Sound(autosquare(78, notetime))
	screensurf.blit(perc12tx, (460, 580))
	pygame.display.update()
	snf4=pygame.mixer.Sound(autosquare(82, notetime))
	snf5=pygame.mixer.Sound(autosquare(87, notetime))
	snf5b=pygame.mixer.Sound(autosquare(92, notetime))
	snf6=pygame.mixer.Sound(autosquare(98, notetime))
	screensurf.blit(perc25tx, (460, 580))
	pygame.display.update()
	snf7=pygame.mixer.Sound(autosquare(104, notetime))
	snf8=pygame.mixer.Sound(autosquare(110, notetime))
	snf9=pygame.mixer.Sound(autosquare(116, notetime))
	snf9=pygame.mixer.Sound(autosquare(116, notetime))
	snf10=pygame.mixer.Sound(autosquare(123, notetime))
	screensurf.blit(perc37tx, (460, 580))
	pygame.display.update()
	snf11=pygame.mixer.Sound(autosquare(131, notetime))
	snf12=pygame.mixer.Sound(autosquare(139, notetime))
	snf13=pygame.mixer.Sound(autosquare(147, notetime))
	snf14=pygame.mixer.Sound(autosquare(156, notetime))
	snf15=pygame.mixer.Sound(autosquare(165, notetime))
	screensurf.blit(perc50tx, (460, 580))
	pygame.display.update()
	snf16=pygame.mixer.Sound(autosquare(175, notetime))
	snf17=pygame.mixer.Sound(autosquare(185, notetime))
	snf18=pygame.mixer.Sound(autosquare(196, notetime))
	snf19=pygame.mixer.Sound(autosquare(208, notetime))
	screensurf.blit(perc62tx, (460, 580))
	pygame.display.update()
	snf19=pygame.mixer.Sound(autosquare(208, notetime))
	snf=pygame.mixer.Sound(autosquare(220, notetime))
	
	snf20=pygame.mixer.Sound(autosquare(233, notetime))
	snf21=pygame.mixer.Sound(autosquare(247, notetime))
	snf22=pygame.mixer.Sound(autosquare(262, notetime))
	screensurf.blit(perc75tx, (460, 580))
	pygame.display.update()
	snf23=pygame.mixer.Sound(autosquare(277, notetime))
	snf24=pygame.mixer.Sound(autosquare(294, notetime))
	snf25=pygame.mixer.Sound(autosquare(311, notetime))
	screensurf.blit(perc87tx, (460, 580))
	pygame.display.update()
	snf26=pygame.mixer.Sound(autosquare(330, notetime))
	snf27=pygame.mixer.Sound(autosquare(349, notetime))
	snf28=pygame.mixer.Sound(autosquare(370, notetime))
	snf29=pygame.mixer.Sound(autosquare(392, notetime))
	pygame.event.clear()



def setnotevols():
	for snd in [snf, snf0, snf1, snf2, snf3, snf4, snf5, snf5b, snf6, snf7, snf8, snf9, snf10, snf11, snf12, snf13, snf14, snf15, snf16, snf17, snf18, snf19, snf20, snf21, snf22, snf23, snf24, snf25, snf26, snf27, snf28, snf29]:
		if stackit==1:
			snd.set_volume((notevol))
		if stackit==2:
			snd.set_volume((notevol/1.3))
		if stackit==3:
			snd.set_volume((notevol/1.5))
		if stackit==4:
			snd.set_volume((notevol/1.6))
		if stackit==5:
			snd.set_volume((notevol/1.7))
notevol=0.5

notestack=1

def meanx(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
def absx(numbers):
	return abs(sum(numbers))
def abssubx(numbers):
	return abs(numbers[0] - sum(numbers[1:]))
mean=meanx
meanflg=0
def noteplay(notesnd):
	if notestack==1:
		notesnd.play(-1, fade_ms=fadeintime)
	if notestack==2:
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(retrigtime)
		notesnd.play(-1, fade_ms=fadeintime)
	if notestack==3:
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(retrigtime)
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(retrigtime)
		notesnd.play(-1, fade_ms=fadeintime)
	if notestack==4:
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(retrigtime)
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(retrigtime)
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(retrigtime)
		notesnd.play(-1, fade_ms=fadeintime)
	if notestack==5:
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(retrigtime)
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(retrigtime)
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(retrigtime)
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(retrigtime)
		notesnd.play(-1, fade_ms=fadeintime)
	if notestack==6:
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(retrigtime)
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(retrigtime)
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(retrigtime)
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(retrigtime)
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(retrigtime)
		notesnd.play(-1, fade_ms=fadeintime)
def notepop(notesnd):
	if notestack==1:
		noteplay(notesnd)
	else:
		notethread = Thread(target = noteplay, args = [notesnd])
		notethread.start()

evhappenflg2=0
cpytx=simplefont.render("Copyright (c) 2016-2018 Thomas Leathers, See readme.md for details.", True, (0, 0, 0))
verstx=simplefont.render("v2.8", True, (0, 0, 0))
bgimg.blit(verstx, (2, 2))
bgimg.blit(cpytx, (2, 22))
txtx1=simplefont.render("Use keys q-],2,3, 5-7, 9,0, + and z-?/, s,d,g-k, l,: to play.", True, (0, 0, 0))
txtx2=simplefont.render("shift+1,2,3,4, or 5 controls octave stacking.", True, (0, 0, 0))
txtx2b=simplefont.render("CTRL+(-),0,1,2,3, or 4 controls octave shift.", True, (0, 0, 0))
txtx2c=simplefont.render("Shift + A,S,D,F,G,H controls Stack Synth ", True, (0, 0, 0))
txtx2bc=simplefont.render("ALT+shift+1,2,3 controls multi-trigger", True, (0, 0, 0))
txtx6=simplefont.render("shift+z,x,c,v,b,n,m controls square method", True, (0, 0, 0))
txtx7=simplefont.render("shift+q,w,e,r controls basewave", True, (0, 0, 0))
txtx1c=simplefont.render("Escape Quits", True, (0, 0, 0))
txtx3b=simplefont.render("(hold shift for fine control)", True, (0, 0, 0))
txtx3=simplefont.render("Use up and down arrow keys to control fade-out.", True, (0, 0, 0))
txtx4=simplefont.render("Use pageup and pagedown to control note volume.", True, (0, 0, 0))
txtx5=simplefont.render("Use left and right arrow keys to control fade-in.", True, (0, 0, 0))
txtx6=simplefont.render("Use Home and End keys to control multi-trigger delay", True, (0, 0, 0))
txtx8=simplefont.render("Use CTRL + PgUp and PgDn to control stack multi. mod.", True, (0, 0, 0))
txtx9=simplefont.render("Use alt+shift + z,x,c,v,b to control aux function.", True, (0, 0, 0))
bgimg.blit(txtx1, (2, 62))
bgimg.blit(txtx2, (2, 82))
bgimg.blit(txtx2b, (2, 102))
bgimg.blit(txtx1c, (400, 62))
bgimg.blit(txtx2c, (400, 82))
bgimg.blit(txtx2bc, (400, 102))
#bgimg.blit(txtx6, (400, 122))
bgimg.blit(txtx7, (400, 122))
bgimg.blit(txtx8, (400, 142))
bgimg.blit(txtx9, (400, 162))
bgimg.blit(txtx3b, (2, 122))
bgimg.blit(txtx4, (2, 142))
bgimg.blit(txtx3, (2, 162))
bgimg.blit(txtx5, (2, 182))
bgimg.blit(txtx6, (2, 202))
fadeintime=0

stm1=simplefont.render(("Stack Synth: Additive"), True, (255, 255, 255))
stm2=simplefont.render(("Stack Synth: Subtractive"), True, (255, 255, 255))
stm3=simplefont.render(("Stack Synth: adsub1"), True, (255, 255, 255))
stm4=simplefont.render(("Stack Synth: Add function"), True, (255, 255, 255))
stm5=simplefont.render(("Stack Synth: Sub function"), True, (255, 255, 255))
stm6=simplefont.render(("Stack Synth: function"), True, (255, 255, 255))
ws1=simplefont.render(("square method: floor"), True, (255, 255, 255))
ws2=simplefont.render(("square method: ceiling"), True, (255, 255, 255))
ws3=simplefont.render(("square method: vstroke"), True, (255, 255, 255))
ws4=simplefont.render(("square method: Two Way"), True, (255, 255, 255))
ws5=simplefont.render(("square method: cstroke"), True, (255, 255, 255))
ws6=simplefont.render(("square method: wstroke"), True, (255, 255, 255))
ws7=simplefont.render(("square method: Three Way"), True, (255, 255, 255))
wm1=simplefont.render(("Wave basetype: sin"), True, (255, 255, 255))
wm2=simplefont.render(("Wave basetype: tan"), True, (255, 255, 255))
wm3=simplefont.render(("Wave basetype: cos+sin"), True, (255, 255, 255))
wm4=simplefont.render(("Wave basetype: tan+sin"), True, (255, 255, 255))
af0=simplefont.render(("aux function: mean"), True, (255, 255, 255))
af1=simplefont.render(("aux function: max"), True, (255, 255, 255))
af2=simplefont.render(("aux function: min"), True, (255, 255, 255))
af3=simplefont.render(("aux function: abs sum"), True, (255, 255, 255))
af4=simplefont.render(("aux function: abs subtract"), True, (255, 255, 255))

sam1=simplefont.render(("Press enter/return to update samples!"), True, (0, 0, 0), (255, 127, 127))
sam2=simplefont.render(("Samples are updated."), True, (255, 255, 255))
def dispupdate():
	notevtx=simplefont.render(("Note Vol: " + str(notevol)), True, (255, 255, 255))
	fadetx=simplefont.render(("Note fadeout time: " + str(fadex)), True, (255, 255, 255))
	fadeintx=simplefont.render(("Note fadein time: " + str(fadeintime)), True, (255, 255, 255))
	stackintx=simplefont.render(("Octave Stacking: " + str(stackit)), True, (255, 255, 255))
	octshifttx=simplefont.render(("Octave Shift: " + str(octshift)), True, (255, 255, 255))
	multrigtx=simplefont.render(("Key multi-trigger: " + str(notestack)), True, (255, 255, 255))
	arlimtx=simplefont.render(("multi-trigger delay: " + str(retrigtime)), True, (255, 255, 255))
	stacksubtx=simplefont.render(("Stack Multiplier mod: " + str(stacksub)), True, (255, 255, 255))
	if stackmod==1:
		stacksyntx=stm1
	elif stackmod==3:
		stacksyntx=stm3
	elif stackmod==4:
		stacksyntx=stm4
	elif stackmod==5:
		stacksyntx=stm5
	elif stackmod==6:
		stacksyntx=stm6
	else:
		stacksyntx=stm2
	if sampup==1:
		syntx=sam1
	else:
		syntx=sam2
	if strexmd==1:
		wstx=ws1
	elif strexmd==3:
		wstx=ws3
	elif strexmd==4:
		wstx=ws4
	elif strexmd==5:
		wstx=ws5
	elif strexmd==6:
		wstx=ws6
	elif strexmd==7:
		wstx=ws7
	else:
		wstx=ws2
	if wavemode==1:
		wmtx=wm1
	elif wavemode==3:
		wmtx=wm3
	elif wavemode==4:
		wmtx=wm4
	else:
		wmtx=wm2
	if meanflg==0:
		auxfx=af0
	elif meanflg==1:
		auxfx=af1
	elif meanflg==3:
		auxfx=af3
	elif meanflg==4:
		auxfx=af4
	else:
		auxfx=af2
	screensurf.blit(bgimg, (0, 0))
	screensurf.blit(stacksyntx, (2, 480))
	screensurf.blit(stackintx, (2, 500))
	screensurf.blit(octshifttx, (2, 520))
	screensurf.blit(wstx, (2, 540))
	screensurf.blit(wmtx, (2, 560))
	screensurf.blit(arlimtx, (2, 580))
	screensurf.blit(multrigtx, (200, 480))
	screensurf.blit(fadetx, (200, 520))
	screensurf.blit(fadeintx, (200, 540))
	screensurf.blit(notevtx, (200, 500))
	screensurf.blit(syntx, (200, 580))
	screensurf.blit(auxfx, (400, 500))
	screensurf.blit(stacksubtx, (400, 480))
	drawwave()
	pygame.display.update()

#waveform drawing function.
def drawwave():
	xpos=2
	xjump=400.0/len(WAVDRAW)
	yposbase=400
	yposmag=0.005
	oldxpos=0
	oldypos=0
	vlinecnt=0
	vlineinterv=60
	pygame.draw.rect(screensurf, (0, 0, 0), pygame.Rect(0, yposbase-60, 401, 121))
	for x in WAVDRAW:
		if vlinecnt<vlineinterv:
			vlinecnt+=1
		else:
			vlinecnt=0
			pygame.draw.line(screensurf, (0, 0, 150), (xpos, yposbase-60), (xpos, yposbase+60))
		xpos+=xjump
	xpos=2		
	
	pygame.draw.line(screensurf, (0, 255, 0), (0, yposbase), (400, yposbase))
	
	for x in WAVDRAW:
		xmag=x*yposmag
		if xmag>60:
			xmag=60
		if xmag<-60:
			xmag=-60
		pygame.draw.line(screensurf, (255, 0, 0), (oldxpos, (oldypos+yposbase)), (xpos, (xmag+yposbase)))
		oldypos=xmag
		oldxpos=xpos
		xpos+=xjump

sampup=0
redefsounds()
setnotevols()
dispupdate()
fscreen=0
while evhappenflg2==0:
		time.sleep(.001)
		keycheckoff()
		
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_RETURN:
				if sampup==1:
					redefsounds()
					setnotevols()
					sampup=0
					dispupdate()
			if event.type == KEYDOWN and event.key == K_SPACE:
				pygame.mixer.stop()
			if event.type == KEYDOWN and event.key == K_F1:
				if fscreen==0:
					screensurf=pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
					fscreen=1
					dispupdate()
				else:
					screensurf=pygame.display.set_mode((800, 600))
					fscreen=0
					dispupdate()
			if (pygame.key.get_mods() & pygame.KMOD_ALT) and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
				if event.type == KEYDOWN and event.key == K_z:
					if meanflg!=0:
						mean=meanx
						meanflg=0
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_x:
					if meanflg!=1:
						meanflg=1
						mean=max
						sampup=1
						dispupdate()
				
				if event.type == KEYDOWN and event.key == K_c:
					if meanflg!=2:
						meanflg=2
						mean=min
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_v:
					if meanflg!=3:
						meanflg=3
						mean=absx
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_b:
					if meanflg!=4:
						meanflg=4
						mean=abssubx
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_1:
					if notestack!=1:
						notestack=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_2:
					if notestack!=2:
						notestack=2
						dispupdate()
				if event.type == KEYDOWN and event.key == K_3:
					if notestack!=3:
						notestack=3
						dispupdate()
				if event.type == KEYDOWN and event.key == K_4:
					if notestack!=4:
						notestack=4
						dispupdate()
				if event.type == KEYDOWN and event.key == K_5:
					if notestack!=5:
						notestack=5
						dispupdate()
				if event.type == KEYDOWN and event.key == K_6:
					if notestack!=6:
						notestack=6
						dispupdate()
			elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
				if event.type == KEYDOWN and event.key == K_1:
					if stackit!=1:
						stackit=1
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_2:
					if stackit!=2:
						stackit=2
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_3:
					if stackit!=3:
						stackit=3
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_4:
					if stackit!=4:
						stackit=4
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_5:
					if stackit!=5:
						stackit=5
						
						sampup=1
						dispupdate()
						
				#wavemode
				if event.type == KEYDOWN and event.key == K_q:
					if wavemode!=1:
						wavemode=1
						foobsin=foobsin1
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_w:
					if wavemode!=2:
						wavemode=2
						foobsin=foobsin2
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_e:
					if wavemode!=3:
						wavemode=3
						foobsin=foobsin3
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_r:
					if wavemode!=4:
						wavemode=4
						foobsin=foobsin4
						sampup=1
						dispupdate()
				#wavesqmode
				if event.type == KEYDOWN and event.key == K_z:
					if strexmd!=1:
						strexmd=1
						#foobsin=foobsin1
						strex=math.floor
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_x:
					if strexmd!=2:
						strexmd=2
						#foobsin=foobsin2
						strex=math.ceil
						sampup=1
						dispupdate()
				
				if event.type == KEYDOWN and event.key == K_c:
					if strexmd!=3:
						strexmd=3
						#foobsin=foobsin2
						strex=vstroke
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_v:
					if strexmd!=4:
						strexmd=4
						#foobsin=foobsin2
						strex=two_way
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_b:
					if strexmd!=5:
						strexmd=5
						#foobsin=foobsin2
						strex=cstroke
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_n:
					if strexmd!=6:
						strexmd=6
						#foobsin=foobsin2
						strex=wstroke
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_m:
					if strexmd!=7:
						strexmd=7
						#foobsin=foobsin2
						strex=three_way
						sampup=1
						dispupdate()
				#stackmode
				if event.type == KEYDOWN and event.key == K_a:
					if stackmod!=1:
						stackmod=1
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_s:
					if stackmod!=2:
						stackmod=2
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_d:
					if stackmod!=3:
						stackmod=3
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_f:
					if stackmod!=4:
						stackmod=4
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_g:
					if stackmod!=5:
						stackmod=5
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_h:
					if stackmod!=6:
						stackmod=6
						
						sampup=1
						dispupdate()
			elif pygame.key.get_mods() & pygame.KMOD_CTRL:
				if event.type == KEYDOWN and (event.key == K_PAGEUP or event.key == K_KP9):
					stacksub += 0.1
					if stacksub>10.0:
						stacksub=10.0
					sampup=1
					dispupdate()
				if event.type == KEYDOWN and (event.key == K_PAGEDOWN or event.key == K_KP3):
					stacksub -= 0.1
					if stacksub<0.1:
						stacksub=0.1
					sampup=1
					dispupdate()
				if event.type == KEYDOWN and event.key == K_1:
					if octshift!=1:
						octshift=1
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_2:
					if octshift!=2:
						octshift=2
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_3:
					if octshift!=3:
						octshift=3
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_4:
					if octshift!=4:
						octshift=4
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_5:
					if octshift!=5:
						octshift=5
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_6:
					if octshift!=6:
						octshift=6
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_7:
					if octshift!=7:
						octshift=7
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_8:
					if octshift!=8:
						octshift=8
						
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_0:
					if octshift!=0:
						octshift=0
						sampup=1
						dispupdate()
				if event.type == KEYDOWN and event.key == K_MINUS:
					if octshift!=-1:
						octshift=-1
						sampup=1
						dispupdate()
				
			else:
				
				if event.type == KEYDOWN and event.key == K_z:
					notepop(snf0)
				if event.type == KEYDOWN and event.key == K_s:
					notepop(snf1)
				if event.type == KEYDOWN and event.key == K_x:	
					notepop(snf2)
				if event.type == KEYDOWN and event.key == K_d:
					notepop(snf3)
				if event.type == KEYDOWN and event.key == K_c:
					notepop(snf4)
				if event.type == KEYDOWN and event.key == K_v:
					notepop(snf5)
				if event.type == KEYDOWN and event.key == K_g:
					notepop(snf5b)
				if event.type == KEYDOWN and event.key == K_b:
					notepop(snf6)
				if event.type == KEYDOWN and event.key == K_h:
					notepop(snf7)
				if event.type == KEYDOWN and event.key == K_n:
					notepop(snf8)
				if event.type == KEYDOWN and event.key == K_j:
					notepop(snf9)
				if event.type == KEYDOWN and event.key == K_m:
					notepop(snf10)
				if event.type == KEYDOWN and (event.key == K_q or event.key == K_LESS or event.key == K_COMMA):
					notepop(snf11)
				if event.type == KEYDOWN and (event.key == K_2 or event.key == K_l):
					notepop(snf12)
				if event.type == KEYDOWN and (event.key == K_w or event.key == K_GREATER or event.key == K_PERIOD):
					notepop(snf13)
				if event.type == KEYDOWN and (event.key == K_3 or event.key == K_COLON or event.key == K_SEMICOLON):
					notepop(snf14)
				if event.type == KEYDOWN and (event.key == K_e or event.key == K_SLASH or event.key == K_QUESTION):
					notepop(snf15)
				if event.type == KEYDOWN and event.key == K_r:
					notepop(snf16)
				if event.type == KEYDOWN and event.key == K_5:
					notepop(snf17)
				if event.type == KEYDOWN and event.key == K_t:
					notepop(snf18)
				if event.type == KEYDOWN and event.key == K_6:
					notepop(snf19)
				if event.type == KEYDOWN and event.key == K_y:
					notepop(snf)
				if event.type == KEYDOWN and event.key == K_7:
					notepop(snf20)
				if event.type == KEYDOWN and event.key == K_u:
					notepop(snf21)
				if event.type == KEYDOWN and event.key == K_i:
					notepop(snf22)
				if event.type == KEYDOWN and event.key == K_9:
					notepop(snf23)
				if event.type == KEYDOWN and event.key == K_o:
					notepop(snf24)
				if event.type == KEYDOWN and event.key == K_0:
					notepop(snf25)
				if event.type == KEYDOWN and event.key == K_p:
					notepop(snf26)
				if event.type == KEYDOWN and event.key == K_LEFTBRACKET:
					notepop(snf27)
				if event.type == KEYDOWN and (event.key == K_EQUALS or event.key == K_PLUS):
					notepop(snf28)
				if event.type == KEYDOWN and event.key == K_RIGHTBRACKET:
					notepop(snf29)
			keycheckoff()
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				evhappenflg2=1
				break
			if pygame.key.get_mods() & pygame.KMOD_SHIFT:
				if event.type == KEYDOWN and (event.key == K_UP or event.key == K_KP8):
					fadex += 10
					dispupdate()
					fadetime=fadex
				if event.type == KEYDOWN and (event.key == K_DOWN or event.key == K_KP2):
					fadex -= 10
					if fadex<0:
						fadex=0
					dispupdate()
					fadetime=fadex
				if event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_KP6):
					fadeintime += 10
					dispupdate()
				if event.type == KEYDOWN and (event.key == K_LEFT or event.key == K_KP4):
					fadeintime -= 10
					if fadeintime<0:
						fadeintime=0
					dispupdate()
				if event.type == KEYDOWN and (event.key == K_PAGEUP or event.key == K_KP9) and not pygame.key.get_mods() & pygame.KMOD_CTRL:
					notevol += 0.01
					if notevol>1.0:
						notevol=1.0
					setnotevols()
					dispupdate()
				if event.type == KEYDOWN and (event.key == K_PAGEDOWN or event.key == K_KP3) and not pygame.key.get_mods() & pygame.KMOD_CTRL:
					notevol -= 0.01
					if notevol<0.1:
						notevol=0.1
					setnotevols()
					dispupdate()
				if event.type == KEYDOWN and (event.key == K_HOME or event.key == K_KP7):
					retrigtime += 0.01
					#setnotevols()
					dispupdate()
				if event.type == KEYDOWN and (event.key == K_END or event.key == K_KP1):
					retrigtime -= 0.01
					if retrigtime<0.01:
						retrigtime=0.01
					
					#setnotevols()
					dispupdate()
			else:
				
				if event.type == KEYDOWN and (event.key == K_UP or event.key == K_KP8):
					fadex += 100
					dispupdate()
					fadetime=fadex
				if event.type == KEYDOWN and (event.key == K_DOWN or event.key == K_KP2):
					fadex -= 100
					if fadex<0:
						fadex=0
					dispupdate()
					fadetime=fadex
				if event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_KP6):
					fadeintime += 100
					dispupdate()
				if event.type == KEYDOWN and (event.key == K_LEFT or event.key == K_KP4):
					fadeintime -= 100
					if fadeintime<0:
						fadeintime=0
					dispupdate()
				if event.type == KEYDOWN and (event.key == K_PAGEUP or event.key == K_KP9) and not pygame.key.get_mods() & pygame.KMOD_CTRL:
					notevol += 0.1
					if notevol>1.0:
						notevol=1.0
					setnotevols()
					dispupdate()
				if event.type == KEYDOWN and (event.key == K_PAGEDOWN or event.key == K_KP3) and not pygame.key.get_mods() & pygame.KMOD_CTRL:
					notevol -= 0.1
					if notevol<0.1:
						notevol=0.1
					setnotevols()
					dispupdate()
				if event.type == KEYDOWN and (event.key == K_HOME or event.key == K_KP7):
					retrigtime += 0.1
					#setnotevols()
					dispupdate()
				if event.type == KEYDOWN and (event.key == K_END or event.key == K_KP1):
					retrigtime -= 0.1
					if retrigtime<0.01:
						retrigtime=0.01
					
					#setnotevols()
					dispupdate()
			#if event.type == KEYDOWN and (event.key == K_LSHIFT or event.key == K_RSHIFT):
				#fadetime=fadex
			#if not keypressed[ K_LSHIFT or event.key == K_RSHIFT):
				#fadetime=100
			if event.type == QUIT:
				evhappenflg2=1
				break
