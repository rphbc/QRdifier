# encoding=utf-8
import pyqrcode
from PIL import Image
import zbarlight


# Gera o QRCode
qr_img = pyqrcode.create("Rosemount: 8732 - Flow measure")
qr_img.png("valve.png", scale=12)

# Lê o QRCode gerado
with open('valve.png', 'rb') as image:
    img = Image.open(image)
    img.load()

# Retira a mensagem guardada no QRcode Gerado
codes = zbarlight.scan_codes('qrcode', img)
print('QR Codes: %s' % codes)
