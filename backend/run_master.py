#!/usr/bin/env python2
"""."""
from naoqi import ALProxy
from PIL import Image
import time


class RunMaster(object):
    """."""

    def __init__(self, app):
        """."""
        app.start()
        session = app.session
        self.memory = session.service("ALMemory")


def save_image():
    cam = ALProxy("ALVideoDevice", '192.168.4.100', 9559)
    res = 3
    color_sp = 11

    start = time.time()
    vid_client = cam.subscribe("python_client", res, color_sp, 5)
    im = cam.getImageRemote(vid_client)
    elapsed = time.time() - start
    print("[i] Fetched in: %s" % str(elapsed))
    cam.unsubscribe(vid_client)

    im_w = im[0]
    im_h = im[1]
    arr = im[6]

    im = Image.frombytes("RGB", (im_w, im_h), arr)
    im.save("camshow.png", "PNG")

    im.show()


if __name__ == '__main__':
    #tts = ALProxy("ALTextToSpeech", "192.168.4.102", 9559)
    save_image()
