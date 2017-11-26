import tensorflow as tf
import cv2
import os
import numpy as np

from common import estimate_pose, read_imgfile, draw_humans, preprocess
from networks import get_network

config = tf.ConfigProto()
config.gpu_options.allocator_type = 'BFC'
config.gpu_options.per_process_gpu_memory_fraction = 0.95
config.gpu_options.allow_growth = True

class Classifier:
    def __init__(self):
        self.th = 0.7
        self.stage_level = 6
        self.imgW = 400
        self.imgH = 400
        self.resSuff = 'res.jpg'
        self.sess = tf.Session(config=config)
        self.input_node = tf.placeholder(tf.float32, shape=(1, self.imgH, self.imgW, 3), name='image')
        self.net, _, self.last_layer = get_network('cmu', self.input_node, self.sess)

    def getHumans(self, img):
        preprocessed = preprocess(img, self.imgW, self.imgH)
        run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
        run_metadata = tf.RunMetadata()
        pafMat, heatMat = self.sess.run(
            [
                self.net.get_output(name=self.last_layer.format(stage=self.stage_level, aux=1)),
                self.net.get_output(name=self.last_layer.format(stage=self.stage_level, aux=2))
            ], feed_dict={'image:0': [img]}, options=run_options, run_metadata=run_metadata
        )
        heatMat, pafMat = heatMat[0], pafMat[0]

        humans = estimate_pose(heatMat, pafMat)
        return humans

    def classify(self, path):
        imgPaths = os.listdir(path)
        cnt = 0
        for imgPath in imgPaths:
            tot = 0
            img = read_imgfile(os.path.join(path, imgPath), self.imgW, self.imgH)
            humans = self.getHumans(img)
            imgcv = cv2.imread(os.path.join(path, imgPath))
            res, delta = draw_humans(imgcv, humans)
            tot += delta

            if (len(humans) == 0):
                imgp90 = cv2.flip(cv2.transpose(img), 1)
                humans = self.getHumans(imgp90)
                imgcvp90 = cv2.flip(cv2.transpose(imgcv), 1)
                res, delta = draw_humans(imgcvp90, humans)
                delta = len(humans) - delta
                tot += delta

                imgn90 = cv2.flip(cv2.transpose(img), 0)
                humans = self.getHumans(imgn90)
                imgcvn90 = cv2.flip(cv2.transpose(imgcv), 0)
                res, delta = draw_humans(imgcvn90, humans)
                delta = len(humans) - delta
                tot += delta
            if tot > 0:
                cnt += 1

        print (cnt)
        if cnt >= self.th * len(os.listdir(path)):
            return 1
        return 0
