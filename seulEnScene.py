#!/usr/bin/env python3
from pyluos import Robot
import time
import pygame
import os
os.system("amixer set PCM -- 90%")

def main():
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    print ("pygame started")

    # configuration spectacle
    FLASHDURATION = 1.0 #durée du temps de flash en secondes
    TEMPSPECTACLE = 3600 # en Secondes
    TEMPSFIN = 25.0 # en seconde avant la fin

    FIRSTALERT = 300 # en seconde avant la fin
    FIRSTALERTDURATION = 5 # en seconde

    SECONDALERT = 120 # en seconde avant la fin
    SECONDALERTDURATION = 5 # en seconde

    # sons
    gong_sound = '/home/pi/Desktop/gong.wav'
    stress_sound = '/home/pi/Desktop/stress.wav'
    stop_sound = '/home/pi/Desktop/stop.wav'
    start_sound = '/home/pi/Desktop/start.wav'
    bip_sound = '/home/pi/Desktop/bip.wav'

    # Luos system connection
    print ("robot connection")
    robot = Robot('/dev/ttyAMA0')

    # env variable
    pressed = False
    light = False
    instant = 0.0
    start = False
    first_buzz = -1.0
    end = False
    first_alert = False
    first_alert_stop = False
    second_alert = False
    second_alert_stop = False

    robot.switch_mod.state = True
    time.sleep(2)
    robot.switch_mod.state = False

    while True :
        time.sleep(0.01)
        # ******************* buzzer management ***************************
        if ((pressed == False) and robot.button_mod.pressed):
            light = not light
            if (first_buzz < 0.0) :
                first_buzz = time.time()
            instant = time.time()
            robot.switch_mod.state = light
            if (start):
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(stop_sound))
                start = False
            else :
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(start_sound))
                start = True

        pressed = robot.button_mod.pressed

        if (light and ((time.time() - instant) >= FLASHDURATION)):
            light = False
            robot.switch_mod.state = light

        # ******************** time management *************************
        # temps fin
        if (((time.time() - first_buzz) >= (TEMPSPECTACLE - TEMPSFIN)) and (first_buzz > 0.0)) :
            ratio = ((time.time() - first_buzz - TEMPSPECTACLE + TEMPSFIN) / TEMPSFIN) * 100
            robot.switch_mod.state = True
            if (end == False):
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(stress_sound))
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(bip_sound), loops = -1)
            end = True
            if (ratio > 100.0) :
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(gong_sound))
                pygame.mixer.Channel(2).stop()
                robot.switch_mod.state = False
                time.sleep(5)
                break

        # first alert
        if (((time.time() - first_buzz) >= (TEMPSPECTACLE - FIRSTALERT)) and (first_buzz > 0.0)) :
            if (first_alert == False):
                print ("first alert")
                robot.switch_mod.state = True
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(bip_sound), loops = -1)
                first_alert = True
            if (((time.time() - first_buzz) >= (TEMPSPECTACLE - FIRSTALERT + FIRSTALERTDURATION)) and (first_alert_stop == False)) :
                pygame.mixer.Channel(2).stop()
                robot.switch_mod.state = False
                first_alert_stop = True
                print ("first alert stop")

        # second alert
        if (((time.time() - first_buzz) >= (TEMPSPECTACLE - SECONDALERT)) and (first_buzz > 0.0)) :
            if (second_alert == False):
                print ("second alert")
                robot.switch_mod.state = True
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(bip_sound), loops = -1)
                second_alert = True
            if (((time.time() - first_buzz) >= (TEMPSPECTACLE - SECONDALERT + SECONDALERTDURATION)) and (second_alert_stop == False)) :
                pygame.mixer.Channel(2).stop()
                robot.switch_mod.state = False
                second_alert_stop = True
                print ("second alert stop")

if __name__ == '__main__':
    main()
