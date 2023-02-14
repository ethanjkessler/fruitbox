import numpy as np
import cv2
import pytesseract
import concurrent.futures
import pyscreenshot

BOARD_LEFT = 670
BOARD_TOP = 180
BOARD_RIGHT = 1230
BOARD_BOTTOM = 500

APPLE_DIMS = (33, 33)

GRID_WIDTH = 17
GRID_HEIGHT = 10

def open_board_image():
    return pyscreenshot.grab(bbox=(BOARD_LEFT, BOARD_TOP, BOARD_RIGHT, BOARD_BOTTOM))

def ocr_image(x, y, image):
    value = int(pytesseract.image_to_string(image, config = "--psm 10 outputbase digits").strip())
    return (x, y, value)

def generate_board_from_image_async(image):
    board = np.zeros((GRID_HEIGHT, GRID_WIDTH)).astype('int32')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                left = j * APPLE_DIMS[0]
                top = i * APPLE_DIMS[1]
                right = (j + 1) * APPLE_DIMS[0]
                bottom = (i + 1) * APPLE_DIMS[1]
                im1 = np.array(image.crop((left, top, right, bottom)))
                im1 = im1[:, :, ::-1].copy()
                gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
                gray = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV)[1]
                futures.append(executor.submit(ocr_image, x=i, y=j, image=gray))
            for future in concurrent.futures.as_completed(futures):
                x, y, value = future.result()
                board[x][y] = value
    return board

def get_board():
    image = open_board_image()
    return generate_board_from_image_async(image)