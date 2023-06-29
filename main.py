import argparse
import os
import pathlib

import tools
from exif import Image


def loadargs():
    # define arguments with argparse for programm
    parser = argparse.ArgumentParser(
        prog='ImageReborder',
        description='Programm to reborder images and put the meta data of the shot into the new image',
        epilog='Have fun and be creative :)'
    )

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable debug messages on console')
    parser.add_argument('-o', '--out', action='store', type=pathlib.Path, default='out/',
                        help='Path to out directory for new images')
    parser.add_argument('-i', '--in', action='store', type=pathlib.Path, default=None, dest='input',
                        help='Path to input directory. All images inside will be processed')
    parser.add_argument('-f', '--files', nargs='+', type=argparse.FileType('rb'), default=None,
                        help='List of pictures to process')
    parser.add_argument('-ic', '--image-camera', dest='imagecamera', action='store', required=False, type=str,
                        help='Camera name')
    parser.add_argument('-il', '--image-lens', dest='imagelens', action='store', required=False, type=str,
                        help='Lense name')
    parser.add_argument('-ia', '--image-aperture', dest='imageaperture', action='store', required=False, type=float,
                        help='Aperture used')
    parser.add_argument('-is', '--image-shutterspeed', dest='imageshutter', action='store', required=False, type=float,
                        help='Shutterspeed used')
    parser.add_argument('-if', '--image-focal-length', dest='imagefocallength', action='store', required=False,
                        type=int,  help='Focal length used')
    parser.add_argument('-ii', '--image-iso', dest='imageiso', action='store', required=False,
                        type=int,  help='ISO used')

    return parser.parse_args()


def printmeta(file):
    for k, v in tools.get_exif_from_file(file).items():
        if type(v) is float or type(v) is int:
            print(f'{k:15}: {v}')
        else:
            print(f'{k:15}: {v}')


def printallmeta(file):
    with open(file, 'rb') as img_file:
        image = Image(img_file)

        for k in image.list_all():
            print(f'{k:30}: {image.get(k)}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Load arguments
    args = loadargs()

    if args.imagelens or args.imageaperture or args.imagefocallength or args.imageshutter or args.imagecamera:
        exifoverride = {
            'shutter_speed': args.imageshutter,
            'lens': args.imagelens,
            'aperture': args.imageaperture,
            'focal_length': args.imagefocallength,
            'model': args.imagecamera,
            'iso': args.imageiso
        }
    else:
        exifoverride = None

    if args.files is None and args.input is None:
        raise argparse.ArgumentTypeError('Either files or input directory has to be give. None found.')

    if args.input is not None:
        for file in os.listdir(args.input):
            if file.split('.').pop() != 'jpg':
                continue

            image = f'{args.input}\\{file}'
            tools.reborder(image, tools.get_exif_from_file(image), exifoverride).save(f'{args.out}/{file}')
    else:
        # Reborder all images
        for image in args.files:
            tools.reborder(image, tools.get_exif_from_file(image), exifoverride).save(f'{args.out}/{image.name.split("/").pop()}')
