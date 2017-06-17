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

windowicon=pygame.image.load("icon32.png")
pygame.display.set_icon(windowicon)
screensurf=pygame.display.set_mode((640, 480))
pygame.display.set_caption("Floored Square Simple Synth", "Floored Square Simple Synth")
pygame.font.init()

simplefont = pygame.font.SysFont(None, 22)
bgimg=pygame.image.load("simplesynth.png").convert()

pygame.mixer.init()

def foobsin(num):
	return (math.floor(math.sin(num)) * 4500)

def autosquare(freq, lenth):
	temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

fadex=600
fadetime=fadex
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


def setnotevols():
	for snd in [snf, snf0, snf1, snf2, snf3, snf4, snf5, snf5b, snf6, snf7, snf8, snf9, snf10, snf11, snf12, snf13, snf14, snf15, snf16, snf17, snf18, snf19, snf20, snf21, snf22]:
		snd.set_volume(notevol)
notevol=0.7
setnotevols()

evhappenflg2=0
cpytx=simplefont.render("(c) 2016-2017 Thomas Leathers, See readme.md for details.", True, (0, 0, 0), (192, 192, 255))
verstx=simplefont.render("v1.1", True, (0, 0, 0), (192, 192, 255))
bgimg.blit(verstx, (2, 2))
bgimg.blit(cpytx, (2, 22))
txtx1=simplefont.render("Use keys q-i,2,3, 5-7 and z-m, s,d,g-k to play. ", True, (0, 0, 0), (192, 192, 255))
txtx2=simplefont.render("Escape quits, ", True, (0, 0, 0), (192, 192, 255))
txtx3=simplefont.render("Use up and down arrow keys to control fade-out ", True, (0, 0, 0), (192, 192, 255))
txtx4=simplefont.render("Use pageup and pagedown to control note volume.", True, (0, 0, 0), (192, 192, 255))
txtx5=simplefont.render("Use left and right arrow keys to control fade-in", True, (0, 0, 0), (192, 192, 255))
bgimg.blit(txtx1, (2, 42))
bgimg.blit(txtx2, (2, 62))
bgimg.blit(txtx3, (2, 82))
bgimg.blit(txtx4, (2, 102))
bgimg.blit(txtx5, (2, 122))
fadeintime=0
def dispupdate():
	notevtx=simplefont.render(("Note Vol: " + str(notevol)), True, (0, 0, 0), (192, 192, 255))
	fadetx=simplefont.render(("Note fadeout time: " + str(fadex)), True, (0, 0, 0), (192, 192, 255))
	fadeintx=simplefont.render(("Note fadein time: " + str(fadeintime)), True, (0, 0, 0), (192, 192, 255))
	screensurf.blit(bgimg, (0, 0))
	screensurf.blit(notevtx, (2, 400))
	screensurf.blit(fadetx, (2, 420))
	screensurf.blit(fadeintx, (2, 440))
	pygame.display.update()
dispupdate()
while evhappenflg2==0:
		time.sleep(.001)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_z:
				snf0.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_s:
				snf1.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_x:	
				snf2.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_d:
				snf3.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_c:
				snf4.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_v:
				snf5.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_g:
				snf5b.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_b:
				snf6.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_h:
				snf7.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_n:
				snf8.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_j:
				snf9.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_m:
				snf10.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_q:
				snf11.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_2:
				snf12.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_w:
				snf13.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_3:
				snf14.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_e:
				snf15.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_r:
				snf16.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_5:
				snf17.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_t:
				snf18.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_6:
				snf19.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_y:
				snf.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_7:
				snf20.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_u:
				snf21.play(-1, fade_ms=fadeintime)
			if event.type == KEYDOWN and event.key == K_i:
				snf22.play(-1, fade_ms=fadeintime)
			if fadetime!=0:
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
			else:
				if event.type == KEYUP and event.key == K_z:
					snf0.stop()
				if event.type == KEYUP and event.key == K_s:
					snf1.stop()
				if event.type == KEYUP and event.key == K_x:
					snf2.stop()
				if event.type == KEYUP and event.key == K_d:
					snf3.stop()
				if event.type == KEYUP and event.key == K_c:
					snf4.stop()
				if event.type == KEYUP and event.key == K_v:
					snf5.stop()
				if event.type == KEYUP and event.key == K_g:
					snf5b.stop()
				if event.type == KEYUP and event.key == K_b:
					snf6.stop()
				if event.type == KEYUP and event.key == K_h:
					snf7.stop()
				if event.type == KEYUP and event.key == K_n:
					snf8.stop()
				if event.type == KEYUP and event.key == K_j:
					snf9.stop()
				if event.type == KEYUP and event.key == K_m:
					snf10.stop()
				if event.type == KEYUP and event.key == K_q:
					snf11.stop()
				if event.type == KEYUP and event.key == K_2:
					snf12.stop()
				if event.type == KEYUP and event.key == K_w:
					snf13.stop()
				if event.type == KEYUP and event.key == K_3:
					snf14.stop()
				if event.type == KEYUP and event.key == K_e:
					snf15.stop()
				if event.type == KEYUP and event.key == K_r:
					snf16.stop()
				if event.type == KEYUP and event.key == K_5:
					snf17.stop()
				if event.type == KEYUP and event.key == K_t:
					snf18.stop()
				if event.type == KEYUP and event.key == K_6:
					snf19.stop()
				if event.type == KEYUP and event.key == K_y:
					snf.stop()
				if event.type == KEYUP and event.key == K_7:
					snf20.stop()
				if event.type == KEYUP and event.key == K_u:
					snf21.stop()
				if event.type == KEYUP and event.key == K_i:
					snf22.stop()
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				evhappenflg2=1
				break
			if event.type == KEYDOWN and event.key == K_UP:
				fadex += 100
				dispupdate()
				fadetime=fadex
			if event.type == KEYDOWN and event.key == K_DOWN:
				fadex -= 100
				if fadex<0:
					fadex=0
				dispupdate()
				fadetime=fadex
			if event.type == KEYDOWN and event.key == K_RIGHT:
				fadeintime += 100
				dispupdate()
			if event.type == KEYDOWN and event.key == K_LEFT:
				fadeintime -= 100
				if fadeintime<0:
					fadeintime=0
				dispupdate()
			if event.type == KEYDOWN and event.key == K_PAGEUP:
				notevol += 0.1
				if notevol>1.0:
					notevol=1.0
				setnotevols()
				dispupdate()
			if event.type == KEYDOWN and event.key == K_PAGEDOWN:
				notevol -= 0.1
				if notevol<0.1:
					notevol=0.1
				setnotevols()
				dispupdate()
			#if event.type == KEYDOWN and (event.key == K_LSHIFT or event.key == K_RSHIFT):
				#fadetime=fadex
			#if event.type == KEYUP and (event.key == K_LSHIFT or event.key == K_RSHIFT):
				#fadetime=100
			if event.type == QUIT:
				evhappenflg2=1
				break
