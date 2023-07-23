import io
import os
import secrets
import qrcode
from PIL import Image


def set_output(path: str = "https://www.charitycomms.org.uk/wp-content/uploads/2019/02/placeholder-image-square.jpg"):
    return path


def getpath(ext: str = "jpg"):
    path = f"temp/{secrets.token_hex(16)}.{ext}"
    attempts = 0
    while attempts < 10:
        if not os.path.exists(path):
            return path
        attempts += 1
    raise FileExistsError(
        "Failed to generate a unique filename after multiple attempts.")


def addlogo(path: str, logo: str, qr_image):
    logo = Image.open(logo)
    logo_size = (qr_image.size[0] // 4, qr_image.size[1] // 4)
    logo = logo.resize(logo_size, Image.ANTIALIAS)
    position = ((qr_image.size[0] - logo.size[0]) //
                2, (qr_image.size[1] - logo.size[1]) // 2)
    qr_image.paste(logo, position)
    # qr_image.save(path)
    image_buffer = io.BytesIO()
    qr_image.save(image_buffer, format="JPEG")
    image_buffer.seek(0)
    return image_buffer


def makeqrcode(data: str, format: str, color_setting: dict, logo: str = None):

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    path_str = str(getpath(format.lower()))
    img = qr.make_image(
        fill_color=color_setting['fillcolor'],
        back_color=color_setting['background']
    )
    
    if logo != None:
        output = addlogo(path_str, logo, img)
        return path_str, output
    else:
        # img.save(path_str)
        image_buffer = io.BytesIO()
        img.save(image_buffer, format="JPEG")
        image_buffer.seek(0)
    return path_str, image_buffer