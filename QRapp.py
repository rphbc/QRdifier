import numpy as np
import cv2
import zbarlight
import sys
from PIL import Image
import zbar

cap = cv2.VideoCapture(0)
qrcodepresent = False

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
    image = Image.fromarray(gray)
    width, height = image.size
    zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())

    # Scans the zbar image.
    scanner = zbar.ImageScanner()
    scanner.scan(zbar_image)

    # Prints data from image.
    decoded = [x.data for x in zbar_image]

    if not decoded:
        qrcodepresent = False
    elif not qrcodepresent:
        print(decoded)
        qrcodepresent = True
    # for decoded in zbar_image:
    #     if not decoded:
    #         print('nao tem nada')
    #     if qrcodepresent==False:
    #         qrcodepresent = True
    #         print(decoded.data)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
