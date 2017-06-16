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
pygame.display.init()
screensurf=pygame.display.set_mode((640, 480))
pygame.display.set_caption("Simple Synth", "Simple Synth")
#pygame.font.init()
#simplefont = pygame.font.SysFont(None, 16)
bgimg=pygame.image.load("simplesynth.png").convert()

pygame.mixer.init()

def foobsin(num):
	return (math.floor(math.sin(num)) * 4500)

def autosquare(freq, lenth):
	temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray
fadetime=100
notetime=(0.1)
#Define sounds
snf0=pygame.mixer.Sound(autosquare(65, notetime))
snf1=pygame.mixer.Sound(autosquare(69, notetime))
snf2=pygame.mixer.Sound(autosquare(74, notetime))
snf3=pygame.mixer.Sound(autosquare(78, notetime))
snf4=pygame.mixer.Sound(autosquare(82, notetime))
snf5=pygame.mixer.Sound(autosquare(87, notetime))
snf5b=pygame.mixer.Sound(autosquare(92, notetime))
snf6=pygame.mixer.Sound(autosquare(98, notetime))
snf7=pygame.mixer.Sound(autosquare(104, notetime))
snf8=pygame.mixer.Sound(autosquare(110, notetime))
snf9=pygame.mixer.Sound(autosquare(116, notetime))
snf9=pygame.mixer.Sound(autosquare(116, notetime))
snf10=pygame.mixer.Sound(autosquare(123, notetime))
snf11=pygame.mixer.Sound(autosquare(131, notetime))
snf12=pygame.mixer.Sound(autosquare(139, notetime))
snf13=pygame.mixer.Sound(autosquare(147, notetime))
snf14=pygame.mixer.Sound(autosquare(156, notetime))
snf15=pygame.mixer.Sound(autosquare(165, notetime))
snf16=pygame.mixer.Sound(autosquare(175, notetime))
snf17=pygame.mixer.Sound(autosquare(185, notetime))
snf18=pygame.mixer.Sound(autosquare(196, notetime))
snf19=pygame.mixer.Sound(autosquare(208, notetime))
snf19=pygame.mixer.Sound(autosquare(208, notetime))
snf=pygame.mixer.Sound(autosquare(220, notetime))
snf20=pygame.mixer.Sound(autosquare(233, notetime))
snf21=pygame.mixer.Sound(autosquare(247, notetime))
snf22=pygame.mixer.Sound(autosquare(262, notetime))
screensurf.blit(bgimg, (0, 0))
pygame.display.update()
evhappenflg2=0
while evhappenflg2==0:
		time.sleep(.001)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_z:
				snf0.play(-1)
			if event.type == KEYDOWN and event.key == K_s:
				snf1.play(-1)
			if event.type == KEYDOWN and event.key == K_x:	
				snf2.play(-1)
			if event.type == KEYDOWN and event.key == K_d:
				snf3.play(-1)
			if event.type == KEYDOWN and event.key == K_c:
				snf4.play(-1)
			if event.type == KEYDOWN and event.key == K_v:
				snf5.play(-1)
			if event.type == KEYDOWN and event.key == K_g:
				snf5b.play(-1)
			if event.type == KEYDOWN and event.key == K_b:
				snf6.play(-1)
			if event.type == KEYDOWN and event.key == K_h:
				snf7.play(-1)
			if event.type == KEYDOWN and event.key == K_n:
				snf8.play(-1)
			if event.type == KEYDOWN and event.key == K_j:
				snf9.play(-1)
			if event.type == KEYDOWN and event.key == K_m:
				snf10.play(-1)
			if event.type == KEYDOWN and event.key == K_q:
				snf11.play(-1)
			if event.type == KEYDOWN and event.key == K_2:
				snf12.play(-1)
			if event.type == KEYDOWN and event.key == K_w:
				snf13.play(-1)
			if event.type == KEYDOWN and event.key == K_3:
				snf14.play(-1)
			if event.type == KEYDOWN and event.key == K_e:
				snf15.play(-1)
			if event.type == KEYDOWN and event.key == K_r:
				snf16.play(-1)
			if event.type == KEYDOWN and event.key == K_5:
				snf17.play(-1)
			if event.type == KEYDOWN and event.key == K_t:
				snf18.play(-1)
			if event.type == KEYDOWN and event.key == K_6:
				snf19.play(-1)
			if event.type == KEYDOWN and event.key == K_y:
				snf.play(-1)
			if event.type == KEYDOWN and event.key == K_7:
				snf20.play(-1)
			if event.type == KEYDOWN and event.key == K_u:
				snf21.play(-1)
			if event.type == KEYDOWN and event.key == K_i:
				snf22.play(-1)
			if event.type == KEYUP and event.key == K_z:
				snf0.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_s:
				snf1.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_x:
				snf2.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_d:
				snf3.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_c:
				snf4.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_v:
				snf5.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_g:
				snf5b.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_b:
				snf6.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_h:
				snf7.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_n:
				snf8.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_j:
				snf9.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_m:
				snf10.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_q:
				snf11.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_2:
				snf12.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_w:
				snf13.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_3:
				snf14.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_e:
				snf15.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_r:
				snf16.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_5:
				snf17.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_t:
				snf18.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_6:
				snf19.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_y:
				snf.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_7:
				snf20.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_u:
				snf21.fadeout(fadetime)
			if event.type == KEYUP and event.key == K_i:
				snf22.fadeout(fadetime)
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				evhappenflg2=1
				break
			if event.type == KEYDOWN and (event.key == K_LSHIFT or event.key == K_RSHIFT):
				fadetime=600
			if event.type == KEYUP and (event.key == K_LSHIFT or event.key == K_RSHIFT):
				fadetime=100
			if event.type == QUIT:
				evhappenflg2=1
				break
