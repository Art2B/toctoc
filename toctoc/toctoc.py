#!/usr/bin/env python
# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python toctoc.py start

#standard python libs
import logging
import os
import sys
from time import sleep
from urllib2 import HTTPError
from urllib2 import URLError
import random

#third party libs
import RPi.GPIO as GPIO
from daemon import Daemon
from twitter import *

class App(Daemon):
           
    def run(self):

        while True:
          try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            TOCTOC_PATH = '/usr/share/toctoc/'
            CONSUMER_K3Y = 'WklI49k0O3Z2ZuMKgOQaBg'
            CONSUMER_S3CR3T = 'E27Dt7NnTYVIswqsz4o5r8U1o2VJ0ekbF7vOC1iTlg'
            MY_TWITTER_CREDS = TOCTOC_PATH + '.toctoc_credentials'
            logger.debug("TWITTER CREDS PATH: " + MY_TWITTER_CREDS)
            if not os.path.exists(MY_TWITTER_CREDS):
                  oauth_dance("toctoc", CONSUMER_K3Y, CONSUMER_S3CR3T, MY_TWITTER_CREDS)

            oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

            twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_K3Y, CONSUMER_S3CR3T))
            logger.info('Twitter OAuth successful')

            oldValue = True
            while True:
              value = GPIO.input(14)
              if ( value == False and value != oldValue):
                  os.system('mpg321 ' + TOCTOC_PATH + 'ding.mp3 &')
                  randomstatus = ''.join(random.sample("abcdefghijklmnopqrstuvwxyzčćšđž", 5)) + "ffff! Someone knocked on the door! Who\'s that? #toctoc cc @zsiangle @gabrielstuff @egeoffray @shiyuewang @draga_t @Soixanteci"
                  try:
                    twitter.statuses.update(status=randomstatus)
                  except TwitterHTTPError as e:
                    os.system('mpg321 ' + TOCTOC_PATH + 'what.mp3 &')
                    raise e
                  os.system('mpg321 ' + TOCTOC_PATH + 'what.mp3 &')
                  logger.info(randomstatus)
              oldValue = value
              sleep(0.05);
          except TwitterHTTPError as e:
            logger.error(e)
          except HTTPError as e:
            logger.error(e)
          except URLError as e:
            logger.error(e)
          except EOFError as e:
            logger.error(e)
          except socket.error as e:
            logger.error(e)
          except:
            logger.error("Unexpected error:")
            logger.error(sys.exc_info()[0])
            raise
          sleep(0.1)  

if __name__ == "__main__":
  daemon = App('/tmp/toctoc.pid')

  logger = logging.getLogger("toctoc log")
  logger.setLevel(logging.DEBUG)
  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  handler = logging.FileHandler("/var/log/toctoc/toctoc.log")
  handler.setFormatter(formatter)
  logger.addHandler(handler)

  if len(sys.argv) == 2:
    if 'start' == sys.argv[1]:
      logger.info('start')
      daemon.start()
    elif 'stop' == sys.argv[1]:
      logger.info('stop')
      daemon.stop()
    elif 'restart' == sys.argv[1]:
      logger.info('restart')
      daemon.restart()
    else:
      print "usage: %s start|stop|restart" % sys.argv[0]
      sys.exit(2)
    sys.exit(0)
  else:
    print "usage: %s start|stop|restart" % sys.argv[0]
    sys.exit(2)

