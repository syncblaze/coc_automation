import time

import pyautogui
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
time.sleep(2)


def trophies() -> tuple[int, int, int, int]:
    POS = (112, 136)
    width = 192 - POS[0]
    height = 171 - POS[1]
    x = (POS[0], POS[1], width, height)
    return x

def gold() -> tuple[int, int, int, int]:
    POS = (1656,35)
    width = 1820 - POS[0]
    height = 68 - POS[1]
    x = (POS[0], POS[1], width, height)
    return x

def elexier() -> tuple[int, int, int, int]:
    POS = (1656,120)
    width = 1820 - POS[0]
    height = 156 - POS[1]
    x = (POS[0], POS[1], width, height)
    return x

region = elexier()
screenshot = pyautogui.screenshot(region=region)


def read_trophys():
    screenshot = pyautogui.screenshot(region=region)
    number_text = pytesseract.image_to_string(screenshot)
    try:
        number = float(number_text)
        return number
    except ValueError:
        return None


# Use pytesseract to extract text from the image
number_text = pytesseract.image_to_string(screenshot)

try:
    number = float(number_text)
    print("Read number:", number)
except ValueError:
    print("Failed to convert text to a number.")
