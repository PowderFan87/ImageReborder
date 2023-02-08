import tools
from exif import Image


def printmeta(file):
    for k, v in tools.get_exif_from_file(file).items():
        if type(v) is float or type(v) is int:
            print(f'{k:15}: {v:.2f}')
        else:
            print(f'{k:15}: {v:}')


def printallmeta(file):
    with open(file, 'rb') as img_file:
        image = Image(img_file)

        for k in image.list_all():
            print(f'{k:30}: {image.get(k)}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    printmeta('input/DSC07985.jpg')
    print('####')
    printmeta('input/DSC08219.jpg')
    print('####')
    printmeta('input/DSC08002.jpg')
    print('####')
    printmeta('input/DSC08174.jpg')
    print('####')
    printmeta('input/DSC08187.jpg')
    # printallmeta('input/DSC08187.jpg')
    newimage = tools.reborder('input/DSC07985.jpg', tools.get_exif_from_file('input/DSC07985.jpg'))

    newimage.save('out/test1.jpg')

    newimage = tools.reborder('input/DSC08219.jpg', tools.get_exif_from_file('input/DSC08219.jpg'))

    newimage.save('out/test2.jpg')
