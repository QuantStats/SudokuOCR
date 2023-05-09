import numpy as np
import cv2


EMPTY_PIXEL_THRESHOLD = 10
EMPTY_PIXEL_PERCENTAGE = 0.95

def is_empty(cell): 
    empty_pixels = np.sum(cell <= EMPTY_PIXEL_THRESHOLD)
    total_pixels = cell.size
    empty_pixel_percentage = empty_pixels / total_pixels
    if empty_pixel_percentage > EMPTY_PIXEL_PERCENTAGE:
        return True
    return False


def recognize_digits(cells, digit_recognition_model):
    # Recognize digits in each cell using your digit recognition model
    digits = []

    for cell in cells:
        digit = 0
        # Preprocess the cell image for digit recognition
        # gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
        if is_empty(cell):
            digits.append(digit)
            continue
        blurred = cv2.GaussianBlur(cell, (5, 5), 0)
        thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        thresh = cv2.resize(thresh, (28, 28))
        thresh = thresh.astype("float32") / 255.0
        thresh = np.expand_dims(thresh, axis=-1)

        # find contours in the thresholded cell
        contours, hierarchy = cv2.findContours(thresh.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Use the digit recognition model to predict the digit in the cell
        if len(contours):
            pred = digit_recognition_model.predict(np.array([thresh]))
            digit = np.argmax(pred, axis=1)[0] + 1

        digits.append(digit)

    return digits


def create_board(digits):
    board = np.array(digits).reshape((9, 9))

    return board.astype(int)

