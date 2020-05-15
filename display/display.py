# -*- coding:UTF-8 -*-
import DEV_Config
import OLED_Driver

from PIL import ImageDraw, Image, ImageFont


def update_text(message):

    OLED = OLED_Driver.OLED()
    print ("**********Init OLED**********")
    OLED_ScanDir = OLED_Driver.SCAN_DIR_DFT  # SCAN_DIR_DFT = D2U_L2R
    OLED.OLED_Init(OLED_ScanDir)
    OLED.OLED_Clear()
    image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)
    draw = ImageDraw.Draw(image)
    fnt = ImageFont.truetype('/usr/share/fonts/truetype/droid.ttf', 14)
    draw.text((0, 0), message, font=fnt, fill="White")
    OLED.OLED_ShowImage(image, 0, 0)
