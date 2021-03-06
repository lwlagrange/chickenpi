#!/usr/bin/python
from modules import DEV_Config
from modules import OLED_Driver
from PIL import ImageDraw, Image, ImageFont


def screen():
    OLED = OLED_Driver.OLED()
    OLED_ScanDir = OLED_Driver.SCAN_DIR_DFT  # SCAN_DIR_DFT = D2U_L2R
    OLED.OLED_Init(OLED_ScanDir)
    return OLED


def update_display(OLED, message):
    if OLED:
        image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)
        draw = ImageDraw.Draw(image)
        reading = ImageFont.truetype('/usr/share/fonts/truetype/Arial.ttf', 36)
        title = ImageFont.truetype('/usr/share/fonts/truetype/Arial.ttf', 22)
        draw.text((0, 0), 'ChickenPi', font=title, fill="White")
        draw.text((104, 10), 'v1.2', fill="White")
        draw.text((0, 25), message['datetime'], fill="White")
        draw.text((0, 40), 'Temperature', fill="White")
        draw.text((0, 48), message['temp'], font=reading, fill="White")
        draw.text((0, 82), 'Humidity', fill="White")
        draw.text((0, 88), message['humid'], font=reading, fill="White")
        OLED.OLED_ShowImage(image, 0, 0)
        return OLED
