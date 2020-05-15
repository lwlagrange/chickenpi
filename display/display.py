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
    DEV_Config.Driver_Delay_ms(20)
    image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)  # grayscale (luminance)
    draw = ImageDraw.Draw(image)
    # font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', "White")

    print ("***draw line")
    draw.line([(0, 0), (127, 0)], fill="White", width=1)
    draw.line([(127, 0), (127, 60)], fill="White", width=1)
    draw.line([(127, 60), (0, 60)], fill="White", width=1)
    draw.line([(0, 60), (0, 0)], fill="White", width=1)
    print ("***draw rectangle")
    draw.rectangle([(18, 10), (110, 20)], fill="White")

    print ("***draw text")
    draw.text((33, 22), 'WaveShare ', fill="White")
    draw.text((32, 36), '', fill="White")
    draw.text((28, 48), '1.5inch OLED ', fill="White")

    OLED.OLED_ShowImage(image, 0, 0)

    # oledDisplay = OLED_Driver.OLED()
    # oledDisplay.OLED_Init(OLED_Driver.SCAN_DIR_DFT)
    # DEV_Config.Driver_Delay_ms(20)
    # print "Update text"
    # image = Image.new("L", (oledDisplay.OLED_Dis_Column, oledDisplay.OLED_Dis_Page), 0)  # grayscale (luminance)
    # draw = ImageDraw.Draw(image)
    # draw.text((33, 22), str(message), fill="White")
