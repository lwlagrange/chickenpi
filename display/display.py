# -*- coding:UTF-8 -*-
import DEV_Config
import OLED_Driver

from PIL import ImageDraw, Image


def update_text(message):
    OLED = OLED_Driver.OLED()

    print ("**********Init OLED**********")
    OLED_ScanDir = OLED_Driver.SCAN_DIR_DFT  # SCAN_DIR_DFT = D2U_L2R
    OLED.OLED_Init(OLED_ScanDir)

    # OLED.OLED_Clear()
    DEV_Config.Driver_Delay_ms(5)
    image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)  # grayscale (luminance)
    draw = ImageDraw.Draw(image)
    # font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', "White")

    draw.text((32, 36), message, fill="White")

    OLED.OLED_ShowImage(image, 0, 0)

    # oledDisplay = OLED_Driver.OLED()
    # oledDisplay.OLED_Init(OLED_Driver.SCAN_DIR_DFT)
    # DEV_Config.Driver_Delay_ms(20)
    # print "Update text"
    # image = Image.new("L", (oledDisplay.OLED_Dis_Column, oledDisplay.OLED_Dis_Page), 0)  # grayscale (luminance)
    # draw = ImageDraw.Draw(image)
    # draw.text((33, 22), str(message), fill="White")
