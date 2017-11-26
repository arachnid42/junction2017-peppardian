import argparse
import cv2
import numpy as np
import time
import logging
import os
import _thread
import threading

import tensorflow as tf

from common import CocoPairsRender, CocoColors, preprocess, estimate_pose, draw_humans
from network_cmu import CmuNetwork
from network_mobilenet import MobilenetNetwork
from networks import get_network
from pose_dataset import CocoPoseLMDB

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')


fps_time = 0


def cb_showimg(img, preprocessed, heatMat, pafMat, humans, show_process=False):
    global fps_time

    # display
    image = img
    image_h, image_w = image.shape[:2]
    image = draw_humans(image, humans)

    scale = 480.0 / image_h
    newh, neww = 480, int(scale * image_w + 0.5)

    image = cv2.resize(image, (neww, newh), interpolation=cv2.INTER_AREA)

    if show_process:
        process_img = CocoPoseLMDB.display_image(preprocessed, heatMat, pafMat, as_numpy=True)
        process_img = cv2.resize(process_img, (640, 480), interpolation=cv2.INTER_AREA)

        canvas = np.zeros([480, 640 + neww, 3], dtype=np.uint8)
        canvas[:, :640] = process_img
        canvas[:, 640:] = image
    else:
        canvas = image

    cv2.putText(canvas, "FPS: %f" % (1.0 / (time.time() - fps_time)), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow('openpose', canvas)

    fps_time = time.time()

quit = 0
lock = threading.Lock()
def cap(cam):
    while not quit:
        if not lock.locked():
            cam.grab()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tensorflow Openpose Realtime Webcam')
    parser.add_argument('--input-width', type=int, default=170)
    parser.add_argument('--input-height', type=int, default=170)
    parser.add_argument('--stage-level', type=int, default=6)
    parser.add_argument('--model', type=str, default='cmu', help='cmu / mobilenet / mobilenet_accurate / mobilenet_fast')
    parser.add_argument('--show-process', type=bool, default=False, help='for debug purpose, if enabled, speed for inference is dropped.')
    args = parser.parse_args()

    input_node = tf.placeholder(tf.float32, shape=(1, args.input_height, args.input_width, 3), name='image')

    with tf.Session() as sess:
        net, _, last_layer = get_network(args.model, input_node, sess)

        cam = cv2.VideoCapture(0)
        # cur = 0

        ret_val, img = cam.read()
        logging.info('cam image=%dx%d' % (img.shape[1], img.shape[0]))

        # buffer.append(img)
        # buffer.append(img)
        # cur = 1
        while True:
            worker = threading.Thread(target = cap, args = (cam, ))
            worker.start()

            print ()
            rv = 0

            while lock.locked():
                pass

            lock.acquire()
            while rv == 0:
                rv, img = cam.read()
            lock.release()

            preprocessed = preprocess(img, args.input_width, args.input_height)

            pafMat, heatMat = sess.run(
                [
                    net.get_output(name=last_layer.format(stage=args.stage_level, aux=1)),
                    net.get_output(name=last_layer.format(stage=args.stage_level, aux=2))
                ], feed_dict={'image:0': [preprocessed]}
            )
            heatMat, pafMat = heatMat[0], pafMat[0]

            humans = estimate_pose(heatMat, pafMat)
            cb_showimg(img, preprocessed, heatMat, pafMat, humans, show_process=args.show_process)

            if cv2.waitKey(1) == 27:
                quit = 1
                worker.join()
                break  # esc to quit

    cv2.destroyAllWindows()
