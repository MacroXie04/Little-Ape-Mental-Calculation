import pytesseract
from PIL import Image, ImageDraw, ImageFont
import pyautogui
import mss
import os
from datetime import datetime
import cv2
import time

pyautogui.PAUSE = 0

def capture_screen_from_points(x1, y1, x2, y2, output_dir):
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    existing_files = [f for f in os.listdir(output_dir) if f.startswith('screenshot_') and f.endswith('.png')]
    count = len(existing_files) + 1
    output_path = os.path.join(output_dir, f'screenshot_{count}.png')
    with mss.mss() as sct:
        region = {'left': left, 'top': top, 'width': width, 'height': height}
        screenshot = sct.grab(region)
        img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
        img.save(output_path)
    return output_path


def draw_symbol(symbol, x_start, y_start):
    if symbol not in ['>', '<']:
        print("请输入有效的符号：'>' 或 '<'")
        return

    size = 100  # 像素

    if symbol == '>':
        # 定义大于号的三个点
        points = [
            (x_start, y_start),
            (x_start + size, y_start + size / 2),
            (x_start, y_start + size)
        ]
    else:
        # 定义小于号的三个点
        points = [
            (x_start + size, y_start),
            (x_start, y_start + size / 2),
            (x_start + size, y_start + size)
        ]

    # 移动到起点
    pyautogui.moveTo(points[0][0], points[0][1], duration=0.02)
    # 按下鼠标并绘制第一条线
    pyautogui.mouseDown()
    pyautogui.dragTo(points[1][0], points[1][1], duration=0.02, button='left')
    # 绘制第二条线
    time.sleep(0.05)
    pyautogui.mouseUp()
    time.sleep(0.05)
    pyautogui.mouseDown()
    pyautogui.dragTo(points[2][0], points[2][1], duration=0.02, button='left')
    # 释放鼠标
    pyautogui.mouseUp()

    print(f"已完成绘制符号 '{symbol}'。")


def delete_image(image_path: str) -> bool:
    try:
        if os.path.exists(image_path):
            os.remove(image_path)
            return True
        else:
            return False
    except Exception as e:
        return False

def recognize_digits(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    text = pytesseract.image_to_string(thresh, config=custom_config)
    digits = ''.join(filter(str.isdigit, text))
    return digits


if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
    output_dir = 'screen/'
    print('Start detection screen')
    while range(1):
        image_left = capture_screen_from_points(320, 524, 413, 600, output_dir)
        image_right = capture_screen_from_points(496, 524, 618, 600, output_dir)
        text_right = recognize_digits(image_right)
        text_left = recognize_digits(image_left)

        if text_right.isdigit() and text_left.isdigit():

            if int(text_left) > int(text_right):
                draw_symbol('>', 462, 884)
                time.sleep(0.3)
            if int(text_left) < int(text_right):
                draw_symbol('<', 462, 884)
                time.sleep(0.3)



        else:
            print('NO')

        # break

"""    while input():
        image_left = capture_screen_from_points(320, 524, 413, 600, output_dir)
        image_right = capture_screen_from_points(496, 524, 618, 600, output_dir)
        text_right = recognize_digits(image_right)
        text_left = recognize_digits(image_left)

        if text_right.isdigit() and text_left.isdigit():

            if int(text_left) > int(text_right):
                draw_symbol('>', 318, 834)
            if int(text_left) < int(text_right):
                draw_symbol('<', 318, 834)

        else:
            print('NO')"""

