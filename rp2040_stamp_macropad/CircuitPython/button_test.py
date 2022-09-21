from adafruit_debouncer import Debouncer
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import busio
import digitalio
import displayio
import random
import rp2040_stamp_macropad_board as board
import terminalio
import time

#displayio.release_displays()
#
#spi = busio.SPI(clock=board.LCD_CLK, MOSI=board.LCD_MOSI)
#display_bus = displayio.FourWire(spi, command=board.LCD_DC, chip_select=board.LCD_CS, reset=board.LCD_RST)
#display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

display = board.DISPLAY

splash = displayio.Group()
display.show(splash)

def make_rect(x, y, w, h, c):
    bmp = displayio.Bitmap(w, h, 1)
    pal = displayio.Palette(1)
    pal[0] = c

    tile = displayio.TileGrid(bmp, pixel_shader=pal, x=x, y=y)
    splash.append(tile)

    return pal

bg = make_rect(0, 0, 128, 64, 0)

rect_w = 14
rect_h = 14
grid_x = grid_y = 16
rects = []
for y in range(4):
    for x in range(3):
        r = make_rect(x * grid_x, y * grid_y, rect_w, rect_h, 0xffffff)
        rects.append(r)

rects.append(make_rect(128 // 2 + grid_x * 0, 64 // 2 - rect_h // 2, rect_w, rect_h, 0xffffff))
rects.append(make_rect(128 // 2 + grid_x * 1, 64 // 2 - rect_h // 2, rect_w, rect_h, 0xffffff))
rects.append(make_rect(128 // 2 + grid_x * 2, 64 // 2 - rect_h // 2, rect_w, rect_h, 0xffffff))

btns = []
btns.append(digitalio.DigitalInOut(board.KEY1))
btns.append(digitalio.DigitalInOut(board.KEY2))
btns.append(digitalio.DigitalInOut(board.KEY3))
btns.append(digitalio.DigitalInOut(board.KEY4))
btns.append(digitalio.DigitalInOut(board.KEY5))
btns.append(digitalio.DigitalInOut(board.KEY6))
btns.append(digitalio.DigitalInOut(board.KEY7))
btns.append(digitalio.DigitalInOut(board.KEY8))
btns.append(digitalio.DigitalInOut(board.KEY9))
btns.append(digitalio.DigitalInOut(board.KEY10))
btns.append(digitalio.DigitalInOut(board.KEY11))
btns.append(digitalio.DigitalInOut(board.KEY12))
btns.append(digitalio.DigitalInOut(board.BTN_LEFT))
btns.append(digitalio.DigitalInOut(board.BTN_CENTER))
btns.append(digitalio.DigitalInOut(board.BTN_RIGHT))

bounces = []
for b in btns:
    b.direction = digitalio.Direction.INPUT
    b.pull = digitalio.Pull.UP

    bounces.append(Debouncer(b))

while True:
    for b in bounces:
        b.update()

    for i in range(len(rects)):
        rects[i][0] = 0xffffff if bounces[i].value else 0x000000
