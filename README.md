# Antoine Rabault improvise avec lui-même
This is the Luos Robotics based program of the stage set of "Antoine Rabault improvise avec lui-même" one man show from Antoine Rabault.

More information on Facebook : https://www.facebook.com/antoineimprovise

## Setup

This stage set is composed by :
 - A Raspberry pi 3 Luos Robotics module containing the main python 3 program
 - A power switch Luos Module to control a set of flashing light
 - A button Luos Module to get "play" "pause" instruction during the show from Antoine
 - A power Jack input used to input 12V in the system and power everything
 
This setup have an Audio Jack output to be linked with the sound system of the theater

## The code
This code allow to manage the show from begining to end. In this show Antoine have 1h to improvise alone during 1 hour.
So this code start a timer at the first button push meaning the begin of the show. After this special push of the button, each push create a pause or start effect on the stage set.
At different moment of the end of the show this program create some time end effect.
