import pyautogui
import keyboard
import time

pyautogui.moveTo(100, 500, duratio=1)

time.sleep(2) # 2 seconds

pyautogui.moveTo(500, None, duration=1.5) # uses the same Y as before