#
# Generate images randomly from directory of images
#

import os
import random
import neural_style
from argparse import ArgumentParser
import time
import multiprocessing


def build_parser():
    parser = ArgumentParser()
    parser.add_argument('--input-dir',
                        dest='input_dir',
                        help='directory of input images',
                        required=True)
    parser.add_argument('--output-dir',
                        dest='output_dir',
                        help='directory of output images',
                        required=True)
    parser.add_argument('--count',
                        dest='count',
                        help='number of images to produce (default infinite)',
                        required=False)
    return parser


def list_files(input_dir):
    return [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and f.lower().endswith('.jpg')]


def create_if_needed(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)


def main(argv):
    parser = build_parser()
    options = parser.parse_args(args=argv)

    input_dir = options.input_dir
    input_files = list_files(input_dir)
    output_dir = options.output_dir
    create_if_needed(output_dir)

    done = False
    count = options.count
    if count is not None:
        count = int(count)

    neural_style_home = os.getenv('NEURAL_STYLE_HOME')

    while not done:
        content_file = random.choice(input_files)
        style_file = random.choice(input_files)

        content_name = content_file.split('.')[0]
        style_name = style_file.split('.')[0]

        output_file = content_name + '__' + style_name + '.jpg'
        output_file = os.path.join(output_dir, output_file)
        print('Creating: ' + output_file)

        content_file = os.path.join(input_dir, content_file)
        style_file = os.path.join(input_dir, style_file)

        argv = [
            '--network', os.path.join(neural_style_home, 'imagenet-vgg-verydeep-19.mat'),
            '--content',  content_file,
            '--styles', style_file,
            '--output', output_file
            ]

        start = time.time()
        p = multiprocessing.Process(target=neural_style.main, args=(argv,))
        p.start()
        p.join()
        sys.stderr.write('Total time to create ' + output_file + ' was ' + str(time.time()-start) + 's\n')

        if count is not None:
            count = count - 1
            if count == 0:
                done = True


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
