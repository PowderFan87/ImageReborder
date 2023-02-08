from exif import Image
from PIL import Image as PILImage, ImageDraw, ImageFont


def calc_offset(bg, img):
    img_w, img_h = img
    bg_w, bg_h = bg

    return (bg_w - img_w) // 2, (bg_h - img_h) // 2


def replace_all(text, rep):
    for i, j in rep.items():
        text = text.replace(i, j)

    return text


def get_exif_from_file(file):
    replacements = {
        'Contemporary': 'C'
    }

    with open(file, 'rb') as img_file:
        image = Image(img_file)
        pilimage = PILImage.open(img_file)

        shutterspeed = image.get('exposure_time')

        if shutterspeed < 1:
            shutterspeed = f'1/{shutterspeed*10000:.0f}'
        else:
            shutterspeed = f'{shutterspeed:.0f}'

        return {
            'shutter_speed': shutterspeed,
            'aperture': image.get('f_number'),
            'focal_length': image.get('focal_length_in_35mm_film'),
            'lens': replace_all(image.get('lens_model'), replacements),
            'model': image.get('model'),
            'iso': image.get('photographic_sensitivity'),
            'width': pilimage.width,
            'height': pilimage.height
        }


def reborder(file, meta):
    # 2048x2048
    bgsize = (2048, 2048)
    font = ImageFont.truetype('tools/Roboto-Bold.ttf', size=50)

    newimagebase = PILImage.new(mode='RGBA', size=bgsize, color=(0, 0, 0, 0))
    newimagedraw = ImageDraw.Draw(newimagebase)

    # right side information
    newimagedraw.text((325, 5), f'{meta["lens"]}', (0, 0, 0), font=font)
    newimagedraw.text((1500, 5), f'{meta["model"]}', (0, 0, 0), font=font)

    # left side information
    newimagedraw.text((325, 1985), f'{meta["shutter_speed"]} sec', (0, 0, 0), font=font)
    newimagedraw.text((650, 1985), f'f/{meta["aperture"]:.1f}', (0, 0, 0), font=font)
    newimagedraw.text((825, 1985), f'ISO {meta["iso"]}', (0, 0, 0), font=font)
    newimagedraw.text((1500, 1985), f'{meta["focal_length"]} mm', (0, 0, 0), font=font)

    newimagebase = newimagebase.rotate(90, expand=True)

    newimage = PILImage.new(mode='RGB', size=bgsize, color='white')
    image = PILImage.open(file)

    if meta['width'] >= meta['height']:
        ratio = meta['width'] / 1920
    else:
        ratio = meta['height'] / 1920

    image = image.resize(size=(int(meta['width'] / ratio), int(meta['height'] / ratio)))

    print(bgsize, image.size, calc_offset(bgsize, image.size))

    newimage.paste(PILImage.open('tools/overlay.jpg'))
    newimage.paste(newimagebase, (0, 0), newimagebase)
    newimage.paste(image, calc_offset(bgsize, image.size))

    return newimage
