import scipy
import scipy.io
import numpy as np
from PIL import Image
import tensorflow as tf


TEST_IMAGE = "test-data/P8040039.png"
OUTPUT_IMAGE = "../python.png"
modelPath = "imagenet-vgg-verydeep-19.mat"
learning_rate = 10
beta1 = 0.9
beta2 = 0.999
epsilon = 1e-8
MEAN_PIXEL = [103.939, 116.799, 123.68]


def imread(path):
    img = scipy.misc.imread(path).astype(np.float)
    if len(img.shape) == 2:
        # grayscale
        img = np.dstack((img, img, img))
    elif img.shape[2] == 4:
        # PNG with alpha channel
        img = img[:, :, :3]
    return img


def imsave(path, img):
    img = np.clip(img, 0, 3255).astype(np.uint8)
    Image.fromarray(img).save(path, quality=100)


def load_net(data_path):
    data = scipy.io.loadmat(data_path)
    if not all(i in data for i in ('layers', 'classes', 'normalization')):
        raise ValueError("You're using the wrong VGG19 data. Please follow the instructions in the README to download the correct data.")
    mean = data['normalization'][0][0][0]
    mean_pixel = np.mean(mean, axis=(0, 1))
    weights = data['layers'][0]
    return weights, mean_pixel

def net_preloaded(weights, input_image):
    kernels, _ = weights[0][0][0][0][0]
    kernels = np.transpose(kernels, (1, 0, 2, 3))
    net = _conv_layer(input_image, kernels)

    return net


def _conv_layer(input, weights):
    return tf.nn.conv2d(input, tf.constant(weights), strides=(1, 1, 1, 1), padding='SAME')


def preprocess(image, mean_pixel):
    return image - mean_pixel


def unprocess(image, mean_pixel):
    return image + mean_pixel


def flattenSortAndPrint(a, fn):
    f = open(fn, 'w')
    for x in a.flatten().tolist():
        f.write('%2.8f\n' % x)
    f.close()

def main():
    content = imread(TEST_IMAGE)
    content_pre = np.array([preprocess(content, MEAN_PIXEL)])
    vgg_weights, _ = load_net(modelPath)
    shape = (1,) + content.shape

    g = tf.Graph()
    with g.as_default(), g.device('/cpu:0'), tf.Session() as sess:
        image = tf.placeholder('float', shape=shape)
        net = net_preloaded(vgg_weights, image)
        content_features = net.eval(feed_dict={image: content_pre})
        flattenSortAndPrint(content_features, '../python.txt')

        initial = tf.zeros(shape) * 0.256
        image_var = tf.Variable(initial)
        net = net_preloaded(vgg_weights, image_var)

        loss = (tf.nn.l2_loss(net - content_features) / content_features.size)

        train_step = tf.train.AdamOptimizer(learning_rate, beta1, beta2, epsilon).minimize(loss)
        sess.run(tf.global_variables_initializer())
        train_step.run()

        print("loss=%g" % loss.eval())

        img_out = unprocess(image_var.eval().reshape(shape[1:]), MEAN_PIXEL)
        imsave(OUTPUT_IMAGE, img_out)


main()
