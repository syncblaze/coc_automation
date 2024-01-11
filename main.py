import json
import os
import pathlib
import random
import sys
import threading
import time
from datetime import datetime
import colorama

import keyboard
import pyautogui
import pytesseract
from colorama import Fore, Style

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

with open("ram.json", "r") as f:
    jdata = json.load(f)


ATTACK = (101,962)
ATTACK2 = (1418,705)
WARMACHINE = (325,977)
PLACE_WARMACHINE = (182,541)
PLACE_WARMACHINE2 = (591,91)
CANCEL = (75, 806)
CONFIRM = (1131,678)
GO_HOME = (950,911)

ELIXIR = (1184,33)
COLLECT_EXILIR = (1379,912)
CLOSE_EXILIR = (1605,104)

TROOP = (462,988)


CLOSE_GAME = (1104, 343)
CONFIRM_CLOSE_GAME = (957,586)

OPEN_GAME = (1439,381)
CLOSE_UMFRAGE = (1106,459)

MODE = jdata["mode"]

time.sleep(4)
POS = (112,136)
width = 192 - POS[0]
height = 171 - POS[1]
region = (POS[0], POS[1], width, height)
def read_trophys(mode: int):
    screenshot = pyautogui.screenshot(region=region)
    number_text = pytesseract.image_to_string(screenshot)
    number_text = number_text.replace("\n", "")
    numeric_chars = [char for char in number_text if char.isdigit() or char == '.']
    number_text = ''.join(numeric_chars)
    try:
        number = float(number_text)
        print(Fore.GREEN + str(datetime.now())+ " | Read number: "+ str(number) + " | MODE: "+str(mode))
        return number
    except ValueError:
        path = pathlib.Path(__file__).parent / "tmp" / str(datetime.now().strftime("%m.%d.%Y-%H_%M_%S")+".png")
        screenshot.save(path, "PNG")
        screenshot = pyautogui.screenshot()
        path = pathlib.Path(__file__).parent / "tmp" / str(datetime.now().strftime("%m.%d.%Y-%H_%M_%S")+"-full.png")
        screenshot.save(path, "PNG")
        print(Fore.RED + str(datetime.now())+ " | Failed to convert text to a number." + str(number_text)+" | MODE: "+str(mode))
        return None

index = jdata["index"]
index2 = 0
if False:
    while True:
        print(pyautogui.position())
        time.sleep(1)

def get_coords(coords: tuple, range: int = 5) -> dict:
    return {
        'x': random.randrange(coords[0]-range, coords[0]+range),
        'y': random.randrange(coords[1]-range, coords[1]+range)
    }

def get_time(secs: float) -> float:
    return random.uniform(secs-0.03, secs+0.03)
def close_game():
    sys.exit()


def add_json(trophies: float):
    if not trophies: return
    with open("data.json", "r") as f:
        data = json.load(f)
    data.append({
        "trophies": int(trophies),
        "timestamp": int(time.time()),
        "mode": MODE
    })
    with open("data.json", "w") as f:
        json.dump(data, f,indent=4)
running = True

def long_running_function():
    global running
    global index
    global index2
    global MODE
    while running:
        index += 1
        index2 += 1
        if keyboard.is_pressed("q"):
            sys.exit()
        pyautogui.moveTo(**get_coords(ATTACK),duration=get_time(0.1))
        pyautogui.click(**get_coords(ATTACK))
        pyautogui.moveTo(**get_coords(ATTACK2),duration=get_time(0.1))
        pyautogui.click(**get_coords(ATTACK2))
        pyautogui.moveTo(**get_coords(WARMACHINE),duration=get_time(4.5))
        pyautogui.click(**get_coords(WARMACHINE))
        pyautogui.moveTo(**get_coords(PLACE_WARMACHINE),duration=get_time(0.1))
        pyautogui.click(**get_coords(PLACE_WARMACHINE))
        pyautogui.moveTo(**get_coords(PLACE_WARMACHINE2),duration=get_time(0.1))
        pyautogui.click(**get_coords(PLACE_WARMACHINE2))
        if MODE == 2:
            pyautogui.moveTo(**get_coords(TROOP),duration=get_time(0.1))
            pyautogui.click(**get_coords(TROOP))
            for i in range(0,13):
                time.sleep(0.01)
                pyautogui.moveTo(**get_coords(PLACE_WARMACHINE))
                pyautogui.click(**get_coords(PLACE_WARMACHINE))
                time.sleep(0.01)
                pyautogui.moveTo(**get_coords(PLACE_WARMACHINE2))
                pyautogui.click(**get_coords(PLACE_WARMACHINE2))
            keyboard.send("alt+F4")
            pyautogui.moveTo(OPEN_GAME[0], OPEN_GAME[1],duration=get_time(1.5))
            pyautogui.click(OPEN_GAME[0], OPEN_GAME[1])
            time.sleep(13)
        else:
            pyautogui.moveTo(**get_coords(CANCEL),duration=get_time(0.1))
            pyautogui.click(**get_coords(CANCEL))
            pyautogui.moveTo(**get_coords(CONFIRM),duration=get_time(0.15))
            pyautogui.click(**get_coords(CONFIRM))
            pyautogui.moveTo(**get_coords(GO_HOME),duration=get_time(0.2))
            pyautogui.click(**get_coords(GO_HOME))
            time.sleep(2.5)
        if index % 3 == 0:
            pyautogui.moveTo(**get_coords(ELIXIR,range=2))
            pyautogui.click(**get_coords(ELIXIR,range=2))
            time.sleep(0.5)
            pyautogui.moveTo(**get_coords(COLLECT_EXILIR))
            pyautogui.click(**get_coords(COLLECT_EXILIR))
            time.sleep(0.1)
            pyautogui.moveTo(**get_coords(CLOSE_EXILIR))
            pyautogui.click(**get_coords(CLOSE_EXILIR))
            time.sleep(0.1)
        time.sleep(0.3)
        add_json(read_trophys(MODE))
        if MODE == 1:
            if index2 > 15:
                MODE = 2
                index2 = 0
        else:
            if index2 > 7:
                MODE = 1
                index2 = 0
        with open("ram.json", "w") as f:
            json.dump({
                "index": index,
                "mode": MODE
            }, f,indent=4)


loop_thread = threading.Thread(target=long_running_function)
loop_thread.start()

keyboard.add_hotkey('ctrl+alt+s', lambda: stop_loop())


def stop_loop():
    global running
    print("Stopping the loop...")
    running = False
    sys.exit()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Handle Ctrl+C to exit the program gracefully
    print("Exiting...")
    loop_thread.join()  # Wait for the loop thread to finish
