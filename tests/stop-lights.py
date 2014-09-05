import os
import subprocess
import sys
import pysimpledmx

channelNumber = 24
mydmx = pysimpledmx.DMXConnection("/dev/ttyUSB0")


for i in range(1,channelNumber):
  mydmx.setChannel(i, 0)
mydmx.render()
