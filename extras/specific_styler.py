#
# Generate images randomly from directory of images
#

import os
import neural_style
from argparse import ArgumentParser
import vgg

def build_parser():
    parser = ArgumentParser()
    parser.add_argument('--content',
                        dest='content',
                        required=True)
    parser.add_argument('--style',
                        dest='style',
                        required=True)
    parser.add_argument('--output',
                        dest='output',
                        required=True)
    parser.add_argument('--scale',
                        dest='scale',
                        required=False)
    return parser


def create_if_needed(fn):
    dir = os.path.dirname(fn)
    if dir == '':
        return
    if not os.path.exists(dir):
        os.mkdir(dir)


def main(argv):
    parser = build_parser()
    options = parser.parse_args(args=argv)

    content = options.content
    style = options.style
    scale = options.scale
    output_filename = options.output
    create_if_needed(output_filename)

    neural_style_home = os.getenv('NEURAL_STYLE_HOME')
    if neural_style_home is None:
        print('NEURAL_STYLE_HOME is not set')
      
    vgg_weights, vgg_mean_pixel = vgg.load_net(os.path.join(neural_style_home, 'imagenet-vgg-verydeep-19.mat'))

    argv = [
        '--content', content,
        '--styles', style,
        '--output', output_filename,
        '--style-scales', scale
        ]

    neural_style.main(argv, vgg_weights, vgg_mean_pixel)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
