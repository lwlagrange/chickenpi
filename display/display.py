# -*- coding:UTF-8 -*-
import DEV_Config
import OLED_Driver

from PIL import ImageDraw, Image, ImageFont

def init_display():
    OLED = OLED_Driver.OLED()
    print ("**********Init OLED**********")
    OLED_ScanDir = OLED_Driver.SCAN_DIR_DFT  # SCAN_DIR_DFT = D2U_L2R
    OLED.OLED_Init(OLED_ScanDir)
    return OLED

def update_text(OLED, message):

    image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/Arial.ttf', 36)
    draw.text((0, 2), message['temp'], font=font, fill="White")
    OLED.OLED_ShowImage(image, 0, 0)
