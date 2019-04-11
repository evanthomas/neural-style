#
# Generate images randomly from directory of images
#

import os
import neural_style
from argparse import ArgumentParser


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

    argv = [
        '--network', '/home/evan/neurosim/neural-style/imagenet-vgg-verydeep-19.mat',
        '--content', content,
        '--styles', style,
        '--output', output_filename,
        '--style-scales', scale
        ]

    neural_style.main(argv)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
