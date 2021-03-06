#!/usr/bin/env python
# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python toctoc.py start

#standard python libs
import os
import subprocess
import sys
import time 
import math 
import random

#third party libs
import RPi.GPIO as GPIO
import pysimpledmx

# Variables
TOCTOC_PATH = '/usr/share/toctoc/'
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
Channels = [[0 for x in xrange(4)] for x in xrange(6)]
pushTime = 0
channelNumber = 24
count = 7

#function to light on
def lightOn():
  for i in range(0,6):
    for j in range(0,4):
      choice = random.randint(0,1)
      if(choice==0):
	value=0
      else: 
	value=255
      mydmx.setChannel(Channels[i][j], value)
  mydmx.render()

#function to light off
def lightOff(n):
  for i in (1,n):
    mydmx.setChannel(i, 0, autorender=True)

# Init the Channels array and the lights
for i in range(0,6):
  Channels[i][0]=i+1
  for j in range(1,4):
    Channels[i][j] = count
    count+=1
mydmx = pysimpledmx.DMXConnection("/dev/ttyUSB0")
lightOff(channelNumber)

while True:
  if ( GPIO.input(14) == False ):
    #os.system('mpg321 ' + TOCTOC_PATH + 'ding.mp3 > /dev/null &')
#    with open(os.devnull, "w") as fnull:
#      subprocess.Popen(['mpg321', TOCTOC_PATH + 'ding.mp3'], stdout = fnull, stderr = fnull)
    pushTime = time.time()
    # Put the code to light here
    lightOn()
  now = time.time()
  distance = (now - pushTime)/10.*100
  #print(distance)
  string = "\r["
  if (distance < 1):
    string += "x"
  else:
    string += " "
  string +="]"
  if (distance < 100 and distance > 1):
    for i in range(1, int(math.floor(distance))):
      string += " "
    string += "x"
  sys.stdout.write(string)
  sys.stdout.write("\r\x1b[K"+string)
  sys.stdout.flush()
  time.sleep(0.2)
