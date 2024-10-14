import cv2
import numpy as np
import pyautogui
import pytesseract
import keyboard
import sys
import time
import pygetwindow as gw
import re

pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe' # 设置 tesseract 安装路径
previous_numbers, skip_count, cached_image = None, 0, None

def focus_window(title="BlueStacks App Player", attempts=3):
    window = gw.getWindowsWithTitle(title)
    return any(window and window[0].activate() or window[0].isActive for _ in range(attempts) if time.sleep(0.2) or True)

def preprocess_image(image):
    return cv2.adaptiveThreshold(cv2.convertScaleAbs(image, alpha=1.5, beta=50), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

def extract_valid_numbers(text):
    return [int(num) for num in re.findall(r'\d+', text) if 0 <= int(num) <= 20]

def capture_and_recognize():
    global cached_image
    if not focus_window(): return None
    screenshot = np.array(pyautogui.screenshot(region=(267, 354, 440, 100)))  # 设定截取屏幕区域
    if cached_image is not None and np.array_equal(screenshot, cached_image): return None
    cached_image = screenshot
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    numbers = extract_valid_numbers(pytesseract.image_to_string(preprocess_image(gray), config='--psm 7'))
    return numbers if len(numbers) >= 2 else None

def compare_and_draw(numbers):
    global previous_numbers, skip_count
    skip_count = skip_count + 1 if numbers == previous_numbers else 0
    pyautogui.press("." if numbers[0] > numbers[1] else ",")
    print(f"{numbers[0]} {'>' if numbers[0] > numbers[1] else '<'} {numbers[1]}")
    previous_numbers = numbers

def main():
    keyboard.add_hotkey('shift+enter', sys.exit)
    print("程序启动，按 'Shift + Enter' 退出")
    while True:
        if numbers := capture_and_recognize():
            compare_and_draw(numbers)
        time.sleep(0.3 if numbers == previous_numbers else 0.01)

if __name__ == "__main__":
    main()