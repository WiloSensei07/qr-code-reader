"""
Created on Sat Feb 19 02:46:54 2022

@author: Wilfried S.
"""

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import cv2
from pyzbar.pyzbar import decode
import json
import zlib as z
import base45 as b
import cbor2 as cb
from cose.messages import CoseMessage as c
import pprint


def generate_qrcode():
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data('Wilo')
    # img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(),
    #                     color_mask=RadialGradiantColorMask(), embeded_image_path=logo)
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(),
                        color_mask=RadialGradiantColorMask())
    img.save('myqrcode.png')


def read_qrcode_on_image(path_img):
    img = cv2.imread(path_img)
    d = cv2.QRCodeDetector()
    val, points, qr_code = d.detectAndDecode(img)
    print(f'Data of your QR Code = {val}')
    print(decode(img))
    for code in decode(img):
        print(f'Type : {code.type}')
        print('Données du QR Code : ', code.data.decode('utf-8'))

    return code.data.decode('utf-8')


def decode_data_pass_sanitaire(data):
    if data.startswith('HC1:'):
        data = data[4:]
    decoded = b.b45decode(data)
    decompressed = z.decompress(decoded);
    msg = c.decode(decompressed);
    phdr, uhdr = msg._hdr_repr()
    payload = cb.loads(msg.payload)

    print("\n")
    print("==PHDR==\n")
    pprint.pprint(phdr)
    print("==UHDR==\n")
    pprint.pprint(uhdr)
    # print("==SIGNATURE==\n",msg.signature,"\n")
    print("==PAYLOAD==")
    print(json.dumps(payload, ensure_ascii=False, indent=4))
    print("\n")


# if __name__ == '__main__':
# generate_qrcode("github.png")
#generate_qrcode()
#read_qrcode_on_image('myqrcode.png')
data_cryptee = read_qrcode_on_image('qr-pass.png')
decode_data_pass_sanitaire(data_cryptee)
