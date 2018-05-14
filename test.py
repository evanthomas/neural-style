
import vgg

import tensorflow as tf
import numpy as np
try:
    reduce
except NameError:
    from functools import reduce

CONTENT_LAYERS = ('conv1_1',)

def net_preloaded(weights, input_image):
    net = {}
    current = input_image
    for i, name in enumerate(CONTENT_LAYERS):
        kind = name[:4]
        if kind == 'conv':
            kernels, bias = weights[i][0][0][0][0]
            # matconvnet: weights are [width, height, in_channels, out_channels]
            # tensorflow: weights are [height, width, in_channels, out_channels]
            kernels = np.transpose(kernels, (1, 0, 2, 3))
            bias = bias.reshape(-1)
            current = _conv_layer(current, kernels, bias)
        elif kind == 'relu':
            pass #current = tf.nn.relu(current)
        elif kind == 'pool':
            pass #current = _pool_layer(current, pooling)
        net[name] = current

    return net

def _conv_layer(input, weights, bias):
    conv = tf.nn.conv2d(input, tf.constant(weights), strides=(1, 1, 1, 1), padding='SAME')
    return tf.nn.bias_add(conv, bias)

def contentLoss(contentFeatures, net):
    content_loss = (2 * tf.nn.l2_loss(net['conv1_1'] - contentFeatures) / contentFeatures.size)
    return content_loss

vgg_weights, vgg_mean_pixel = vgg.load_net('imagenet-vgg-verydeep-19.mat')
shape = [1, 100, 100, 3]
contentImage = np.ones(shape)

g = tf.Graph()
with g.as_default(), g.device('/cpu:0'), tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
    pl = tf.placeholder('float', shape=shape)
    net = net_preloaded(vgg_weights, pl)
    contentFeatures = net['conv1_1'].eval(feed_dict={pl: contentImage})

initialImage = tf.zeros(shape)
imageVar = tf.Variable(initialImage)
net = net_preloaded(vgg_weights, imageVar)

cl = contentLoss(contentFeatures, net)

with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
    sess.run(tf.global_variables_initializer())
    l = cl.eval()
    sw = tf.summary.FileWriter('../pythonLogDir', graph=sess.graph)
    print(l)

