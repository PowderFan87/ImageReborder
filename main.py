import argparse
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
    parser.add_argument('-f', '--files', required=True, nargs='+', type=argparse.FileType('rb'),
                        help='List of pictures to process')

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

    # Reborder all images
    for image in args.files:
        tools.reborder(image, tools.get_exif_from_file(image)).save(f'{args.out}/{image.name.split("/").pop()}')
