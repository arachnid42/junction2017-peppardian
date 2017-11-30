#!/usr/bin/env python2
"""."""
from naoqi import ALProxy
from PIL import Image
from image_sender import ImageSender
from make_call import PhoneController
import time
import os


class RunMaster(object):
    """."""

    def __init__(self):
        """."""
        #app.start()
        #session = app.session
        #self.memory = session.service("ALMemory")
        self.ip = '192.168.4.100'
        self.port = 9559

    def set_awereness(self):
        awareness = ALProxy('ALBasicAwareness', self.ip, self.port)
        awareness.setEngagementMode('FullyEngaged')
        awareness.startAwareness()

    def good_reation(self):
        tts = ALProxy('ALAnimatedSpeech', self.ip, self.port)
        tts.post.say('You are definitely OK!!', {"speakingMovementMode": "OfferBothHands_HeadNod_LeanLeft"})


    def show_reaction(self):
        tts = ALProxy('ALAnimatedSpeech', self.ip, self.port)
        tts.post.say('I love Julia Martova!', {"speakingMovementMode": "StrictPointAtUserArm"})

    def save_image(self, counter):
        cam = ALProxy("ALVideoDevice", self.ip, self.port)
        res = 2

        color_sp = 11

        start = time.time()

        vid_client = cam.subscribe("python_client", res, color_sp, 1)
        im = cam.getImageRemote(vid_client)
        if im is None:
            print("Error!")
            cam.unsubscribe(vid_client)
            return
        elapsed = time.time() - start
        print("[i] Fetched in: %s" % str(elapsed))
        cam.unsubscribe(vid_client)

        im_w = im[0]
        im_h = im[1]
        arr = im[6]

        im = Image.frombytes("RGB", (im_w, im_h), arr)
        im.save('images/'+str(counter)+".jpg", "JPEG")


if __name__ == '__main__':
    rm = RunMaster()
    rm.show_reaction()
    im = ImageSender("http://mlgpu1.bitville.com:5555/submit_image")
    pc = PhoneController()
    rm.set_awereness()
    while True:
        for i in range(10):
            rm.save_image(i)
        for image in os.listdir('images/'):
            result = im.send_image('images/'+image)
            print(result)
            if result == 'sick':
                rm.show_reaction()
                pc.make_call('+37256739550')
                pc.send_sms('+37256739550', 'Dipoli\nOtakaari 24\nOtaniemi\n02150 Espoo, Finland')
                break
            elif result == 'ok':
                rm.good_reation()
                break

