import tensorflow as tf
import cv2
import time
import logging
import argparse
import numpy as np

from common import estimate_pose, read_imgfile, draw_humans
from networks import get_network

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

config = tf.ConfigProto()
config.gpu_options.allocator_type = 'BFC'
config.gpu_options.per_process_gpu_memory_fraction = 0.95
config.gpu_options.allow_growth = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tensorflow Openpose Inference')
    parser.add_argument('--imgpath', type=str, default='./test/1.jpg')
    parser.add_argument('--input-width', type=int, default=400)
    parser.add_argument('--input-height', type=int, default=400)
    parser.add_argument('--stage-level', type=int, default=6)
    parser.add_argument('--model', type=str, default='cmu', help='cmu / mobilenet / mobilenet_accurate / mobilenet_fast')
    args = parser.parse_args()

    input_node = tf.placeholder(tf.float32, shape=(1, args.input_height, args.input_width, 3), name='image')

    with tf.Session(config=config) as sess:
        net, _, last_layer = get_network(args.model, input_node, sess)

        logging.debug('read image+')
        image = read_imgfile(args.imgpath, args.input_width, args.input_height)

        a = time.time()
        run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
        run_metadata = tf.RunMetadata()
        pafMat, heatMat = sess.run(
            [
                net.get_output(name=last_layer.format(stage=args.stage_level, aux=1)),
                net.get_output(name=last_layer.format(stage=args.stage_level, aux=2))
            ], feed_dict={'image:0': [image]}, options=run_options, run_metadata=run_metadata
        )
        logging.info('inference- elapsed_time={}'.format(time.time() - a))

        heatMat, pafMat = heatMat[0], pafMat[0]

        logging.info('pose+')
        a = time.time()
        humans = estimate_pose(heatMat, pafMat)
        logging.info('pose- elapsed_time={}'.format(time.time() - a))

        # display
        imagecv = cv2.imread(args.imgpath)
        image_h, image_w = imagecv.shape[:2]
        image, delta = draw_humans(imagecv, humans)
        print (delta)

        # scale = 480.0 / image_h
        # newh, neww = 480, int(scale * image_w + 0.5)

        # image = cv2.resize(image, (neww, newh), interpolation=cv2.INTER_AREA)

        cv2.imshow('result', image)
        cv2.waitKey(0)

        tf.train.write_graph(sess.graph_def, '.', 'graph-tmp.pb', as_text=True)