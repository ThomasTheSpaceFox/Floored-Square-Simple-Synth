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
from threading import Thread
pygame.display.init()

windowicon=pygame.image.load("icon32.png")
pygame.display.set_icon(windowicon)
screensurf=pygame.display.set_mode((640, 480))
pygame.display.set_caption("Floored Square Simple Synth", "Floored Square Simple Synth")
pygame.font.init()

simplefont = pygame.font.SysFont(None, 22)
bgimg=pygame.image.load("simplesynth.jpg").convert()

pygame.mixer.init()

def foobsin(num):
	return (math.floor(math.sin(num)) * 4500)
stackit=1
octshift=1
stackmod=1
def autosquare(freq, lenth):
	if octshift==0:
		freq=(freq//2)
	else:
		freq=(freq*octshift)
	if stackmod==1:
		if stackit==1:
			return autosquare1stack(freq, lenth)
		elif stackit==2:
			return autosquare2stack(freq, lenth)
		elif stackit==3:
			return autosquare3stack(freq, lenth)
		elif stackit==4:
			return autosquare4stack(freq, lenth)
		elif stackit==5:
			return autosquare5stack(freq, lenth)
		else:
			return autosquare1stack(freq, lenth)
	if stackmod==3:
		if stackit==1:
			return autosquare1stack(freq, lenth)
		elif stackit==2:
			return autosquare2stackne(freq, lenth)
		elif stackit==3:
			return autosquare3stacknexq(freq, lenth)
		elif stackit==4:
			return autosquare4stacknexq(freq, lenth)
		elif stackit==5:
			return autosquare5stacknexq(freq, lenth)
		else:
			return autosquare1stack(freq, lenth)
	if stackmod==4:
		if stackit==1:
			return autosquare1stack(freq, lenth)
		elif stackit==2:
			return autosquare2stacksubab(freq, lenth)
		elif stackit==3:
			return autosquare3stacksubab(freq, lenth)
		elif stackit==4:
			return autosquare4stacksubab(freq, lenth)
		elif stackit==5:
			return autosquare5stacksubab(freq, lenth)
		else:
			return autosquare1stack(freq, lenth)
	else:
		if stackit==1:
			return autosquare1stack(freq, lenth)
		elif stackit==2:
			return autosquare2stackne(freq, lenth)
		elif stackit==3:
			return autosquare3stackne(freq, lenth)
		elif stackit==4:
			return autosquare4stackne(freq, lenth)
		elif stackit==5:
			return autosquare5stackne(freq, lenth)
		else:
			return autosquare1stackne(freq, lenth)

def autosquare1stack(freq, lenth):
	temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

def autosquare2stack(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * math.pi * freq * t / 22050) + foobsin(2.0 * math.pi * (freq * 2) * t / 22050))) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

def autosquare3stack(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * math.pi * freq * t / 22050) + foobsin(2.0 * math.pi * (freq * 2) * t / 22050) + foobsin(2.0 * math.pi * (freq * 3) * t / 22050))) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

def autosquare4stack(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * math.pi * freq * t / 22050) + foobsin(2.0 * math.pi * (freq * 2) * t / 22050) + foobsin(2.0 * math.pi * (freq * 3) * t / 22050) + foobsin(2.0 * math.pi * (freq * 4) * t / 22050))) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray
	
def autosquare5stack(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * math.pi * freq * t / 22050) + foobsin(2.0 * math.pi * (freq * 2) * t / 22050) + foobsin(2.0 * math.pi * (freq * 3) * t / 22050) + foobsin(2.0 * math.pi * (freq * 4) * t / 22050) + foobsin(2.0 * math.pi * (freq * 5) * t / 22050))) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

def autosquare2stackne(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * math.pi * freq * t / 22050) - foobsin(2.0 * math.pi * (freq * 2) * t / 22050))) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

def autosquare3stackne(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * math.pi * freq * t / 22050) - foobsin(2.0 * math.pi * (freq * 2) * t / 22050) - foobsin(2.0 * math.pi * (freq * 3) * t / 22050))) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

def autosquare4stackne(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * math.pi * freq * t / 22050) - foobsin(2.0 * math.pi * (freq * 2) * t / 22050) - foobsin(2.0 * math.pi * (freq * 3) * t / 22050) - foobsin(2.0 * math.pi * (freq * 4) * t / 22050))) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

def autosquare5stackne(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * math.pi * freq * t / 22050) - foobsin(2.0 * math.pi * (freq * 2) * t / 22050) - foobsin(2.0 * math.pi * (freq * 3) * t / 22050) - foobsin(2.0 * math.pi * (freq * 4) * t / 22050) - foobsin(2.0 * math.pi * (freq * 5) * t / 22050))) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

def autosquare2stacknexq(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * math.pi * freq * t / 22050) - (foobsin(2.0 * math.pi * (freq * 2) * t / 22050)))) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

def autosquare3stacknexq(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * math.pi * freq * t / 22050) - (foobsin(2.0 * math.pi * (freq * 2) * t / 22050) + foobsin(2.0 * math.pi * (freq * 3) * t / 22050)))) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

def autosquare4stacknexq(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * math.pi * freq * t / 22050) - (foobsin(2.0 * math.pi * (freq * 2) * t / 22050) + foobsin(2.0 * math.pi * (freq * 3) * t / 22050) - foobsin(2.0 * math.pi * (freq * 4) * t / 22050)))) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

def autosquare5stacknexq(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * math.pi * freq * t / 22050) - (foobsin(2.0 * math.pi * (freq * 2) * t / 22050) + foobsin(2.0 * math.pi * (freq * 3) * t / 22050) - foobsin(2.0 * math.pi * (freq * 4) * t / 22050) + foobsin(2.0 * math.pi * (freq * 5) * t / 22050)))) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

def autosquare2stacksubab(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * math.pi * freq * t / 22050) - abs(foobsin(2.0 * math.pi * (freq * 2) * t / 22050)))) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

def autosquare3stacksubab(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * math.pi * freq * t / 22050) - abs(foobsin(2.0 * math.pi * (freq * 2) * t / 22050) + foobsin(2.0 * math.pi * (freq * 3) * t / 22050)))) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

def autosquare4stacksubab(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * math.pi * freq * t / 22050) - abs(foobsin(2.0 * math.pi * (freq * 2) * t / 22050) + foobsin(2.0 * math.pi * (freq * 3) * t / 22050) + foobsin(2.0 * math.pi * (freq * 4) * t / 22050)))) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

def autosquare5stacksubab(freq, lenth):
	temparray=array.array('f', [((foobsin(2.0 * math.pi * freq * t / 22050) - abs(foobsin(2.0 * math.pi * (freq * 2) * t / 22050) + foobsin(2.0 * math.pi * (freq * 3) * t / 22050) + foobsin(2.0 * math.pi * (freq * 4) * t / 22050) + foobsin(2.0 * math.pi * (freq * 5) * t / 22050)))) for t in xrange(0, int(22050))])
	#temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
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


pleasewaittx=simplefont.render("Please wait... Generating samples...", True, (0, 0, 0), (192, 192, 255))
perc0tx=simplefont.render("0%...", True, (0, 0, 0), (192, 192, 255))
perc25tx=simplefont.render("25%...", True, (0, 0, 0), (192, 192, 255))
perc50tx=simplefont.render("50%...", True, (0, 0, 0), (192, 192, 255))
perc75tx=simplefont.render("75%...", True, (0, 0, 0), (192, 192, 255))
#Define sounds
def redefsounds():
	dispupdate()
	screensurf.blit(pleasewaittx, (2, 320))
	screensurf.blit(perc0tx, (2, 340))
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
	snf4=pygame.mixer.Sound(autosquare(82, notetime))
	snf5=pygame.mixer.Sound(autosquare(87, notetime))
	snf5b=pygame.mixer.Sound(autosquare(92, notetime))
	snf6=pygame.mixer.Sound(autosquare(98, notetime))
	screensurf.blit(perc25tx, (2, 340))
	pygame.display.update()
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
	screensurf.blit(perc50tx, (2, 340))
	pygame.display.update()
	snf16=pygame.mixer.Sound(autosquare(175, notetime))
	snf17=pygame.mixer.Sound(autosquare(185, notetime))
	snf18=pygame.mixer.Sound(autosquare(196, notetime))
	snf19=pygame.mixer.Sound(autosquare(208, notetime))
	snf19=pygame.mixer.Sound(autosquare(208, notetime))
	snf=pygame.mixer.Sound(autosquare(220, notetime))
	snf20=pygame.mixer.Sound(autosquare(233, notetime))
	snf21=pygame.mixer.Sound(autosquare(247, notetime))
	snf22=pygame.mixer.Sound(autosquare(262, notetime))
	screensurf.blit(perc75tx, (2, 340))
	pygame.display.update()
	snf23=pygame.mixer.Sound(autosquare(277, notetime))
	snf24=pygame.mixer.Sound(autosquare(294, notetime))
	snf25=pygame.mixer.Sound(autosquare(311, notetime))
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

def noteplay(notesnd):
	if notestack==1:
		notesnd.play(-1, fade_ms=fadeintime)
	if notestack==2:
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(.1)
		notesnd.play(-1, fade_ms=fadeintime)
	if notestack==3:
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(.1)
		notesnd.play(-1, fade_ms=fadeintime)
		time.sleep(.1)
		notesnd.play(-1, fade_ms=fadeintime)
def notepop(notesnd):
	if notestack==1:
		noteplay(notesnd)
	else:
		notethread = Thread(target = noteplay, args = [notesnd])
		notethread.start()

evhappenflg2=0
cpytx=simplefont.render("(c) 2016-2017 Thomas Leathers, See readme.md for details.", True, (0, 0, 0), (192, 192, 255))
verstx=simplefont.render("v2.1", True, (0, 0, 0), (192, 192, 255))
bgimg.blit(verstx, (2, 2))
bgimg.blit(cpytx, (2, 22))
txtx1=simplefont.render("Use keys q-],2,3, 5-7, 9,0, + and z-?/, s,d,g-k, l,: to play. Escape quits.", True, (0, 0, 0), (192, 192, 255))
txtx2=simplefont.render("shift+1,2,3,4, or 5 controls octave stacking, Shift + A,S,D,F controls Stack Synth ", True, (0, 0, 0), (192, 192, 255))
txtx2b=simplefont.render("CTRL+0,1,2,3, or 4 controls octave shift.  ALT+shift+1,2,3 controls multi-trigger", True, (0, 0, 0), (192, 192, 255))
txtx3=simplefont.render("Use up and down arrow keys to control fade-out ", True, (0, 0, 0), (192, 192, 255))
txtx4=simplefont.render("Use pageup and pagedown to control note volume.", True, (0, 0, 0), (192, 192, 255))
txtx5=simplefont.render("Use left and right arrow keys to control fade-in", True, (0, 0, 0), (192, 192, 255))
bgimg.blit(txtx1, (2, 62))
bgimg.blit(txtx2, (2, 82))
bgimg.blit(txtx2b, (2, 102))
bgimg.blit(txtx4, (2, 122))
bgimg.blit(txtx3, (2, 142))
bgimg.blit(txtx5, (2, 162))
fadeintime=0
def dispupdate():
	notevtx=simplefont.render(("Note Vol: " + str(notevol)), True, (0, 0, 0), (192, 192, 255))
	fadetx=simplefont.render(("Note fadeout time: " + str(fadex)), True, (0, 0, 0), (192, 192, 255))
	fadeintx=simplefont.render(("Note fadein time: " + str(fadeintime)), True, (0, 0, 0), (192, 192, 255))
	stackintx=simplefont.render(("Octave Stacking: " + str(stackit)), True, (0, 0, 0), (192, 192, 255))
	octshifttx=simplefont.render(("Octave Shift: " + str(octshift)), True, (0, 0, 0), (192, 192, 255))
	multrigtx=simplefont.render(("Key multi-trigger: " + str(notestack)), True, (0, 0, 0), (192, 192, 255))
	if stackmod==1:
		stacksyntx=simplefont.render(("Stack Synth: Additive"), True, (0, 0, 0), (192, 192, 255))
	if stackmod==3:
		stacksyntx=simplefont.render(("Stack Synth: adsub1"), True, (0, 0, 0), (192, 192, 255))
	if stackmod==4:
		stacksyntx=simplefont.render(("Stack Synth: Sub ABS"), True, (0, 0, 0), (192, 192, 255))
	else:
		stacksyntx=simplefont.render(("Stack Synth: Subtractive"), True, (0, 0, 0), (192, 192, 255))
	screensurf.blit(bgimg, (0, 0))
	screensurf.blit(notevtx, (2, 380))
	screensurf.blit(fadetx, (2, 400))
	screensurf.blit(fadeintx, (2, 420))
	screensurf.blit(stackintx, (2, 440))
	screensurf.blit(octshifttx, (2, 460))
	screensurf.blit(multrigtx, (200, 380))
	screensurf.blit(stacksyntx, (200, 400))
	pygame.display.update()

redefsounds()
setnotevols()
dispupdate()
while evhappenflg2==0:
		time.sleep(.001)
		keycheckoff()
		for event in pygame.event.get():
			if (pygame.key.get_mods() & pygame.KMOD_ALT) and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
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
			elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
				if event.type == KEYDOWN and event.key == K_1:
					if stackit!=1:
						stackit=1
						redefsounds()
						dispupdate()
						setnotevols()
				if event.type == KEYDOWN and event.key == K_2:
					if stackit!=2:
						stackit=2
						redefsounds()
						dispupdate()
						setnotevols()
				if event.type == KEYDOWN and event.key == K_3:
					if stackit!=3:
						stackit=3
						redefsounds()
						dispupdate()
						setnotevols()
				if event.type == KEYDOWN and event.key == K_4:
					if stackit!=4:
						stackit=4
						redefsounds()
						dispupdate()
						setnotevols()
				if event.type == KEYDOWN and event.key == K_5:
					if stackit!=5:
						stackit=5
						redefsounds()
						dispupdate()
						setnotevols()
				if event.type == KEYDOWN and event.key == K_a:
					if stackmod!=1:
						stackmod=1
						redefsounds()
						dispupdate()
						setnotevols()
				if event.type == KEYDOWN and event.key == K_s:
					if stackmod!=2:
						stackmod=2
						redefsounds()
						dispupdate()
						setnotevols()
				if event.type == KEYDOWN and event.key == K_d:
					if stackmod!=3:
						stackmod=3
						redefsounds()
						dispupdate()
						setnotevols()
				if event.type == KEYDOWN and event.key == K_f:
					if stackmod!=4:
						stackmod=4
						redefsounds()
						dispupdate()
						setnotevols()
			elif pygame.key.get_mods() & pygame.KMOD_CTRL:
				if event.type == KEYDOWN and event.key == K_1:
					if octshift!=1:
						octshift=1
						redefsounds()
						dispupdate()
						setnotevols()
				if event.type == KEYDOWN and event.key == K_2:
					if octshift!=2:
						octshift=2
						redefsounds()
						dispupdate()
						setnotevols()
				if event.type == KEYDOWN and event.key == K_3:
					if octshift!=3:
						octshift=3
						redefsounds()
						dispupdate()
						setnotevols()
				if event.type == KEYDOWN and event.key == K_4:
					if octshift!=4:
						octshift=4
						redefsounds()
						dispupdate()
						setnotevols()
				if event.type == KEYDOWN and event.key == K_0:
					if octshift!=0:
						octshift=0
						redefsounds()
						dispupdate()
						setnotevols()
				
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
			if event.type == KEYDOWN and (event.key == K_PAGEUP or event.key == K_KP9):
				notevol += 0.1
				if notevol>1.0:
					notevol=1.0
				setnotevols()
				dispupdate()
			if event.type == KEYDOWN and (event.key == K_PAGEDOWN or event.key == K_KP3):
				notevol -= 0.1
				if notevol<0.1:
					notevol=0.1
				setnotevols()
				dispupdate()
			#if event.type == KEYDOWN and (event.key == K_LSHIFT or event.key == K_RSHIFT):
				#fadetime=fadex
			#if not keypressed[ K_LSHIFT or event.key == K_RSHIFT):
				#fadetime=100
			if event.type == QUIT:
				evhappenflg2=1
				break
