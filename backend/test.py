#!/usr/bin/env python2
#
from naoqi import ALProxy

awareness = ALProxy('ALBasicAwareness')
awareness.setEngagementMode('FullyEngaged')
awareness.startAwareness()

tts = ALProxy("ALTextToSpeech", "192.168.4.102", 9559)
tts.say("Give it to me")

