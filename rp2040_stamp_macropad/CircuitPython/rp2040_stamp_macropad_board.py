import board

KEY3 = board.GP0
KEY2 = board.GP1
KEY1 = board.GP2
KEY6 = board.GP3
KEY5 = board.GP4
KEY4 = board.GP5
KEY9 = board.GP6
KEY8 = board.GP7
KEY7 = board.GP8
NEOPIXEL = board.GP9
KEY12 = board.GP10
KEY11 = board.GP11
KEY10 = board.GP12

LCD_CLK = board.GP22
LCD_MOSI = board.GP23
LCD_DC = board.GP24
LCD_RST = board.GP25
LCD_CS = board.GP26
BTN_RIGHT = board.GP27
BTN_LEFT = board.GP28
BTN_CENTER = board.GP29

BUTTON = BTN_CENTER

SPEAKER_ENABLE = board.GP16

LED = board.GP20

STAMP_NEOPIXEL = board.GP21

ROTA = board.GP13
ROTB = board.GP14
ROTC = board.GP15

import adafruit_displayio_ssd1306
import displayio
import busio

displayio.release_displays()

_spi = busio.SPI(clock=LCD_CLK, MOSI=LCD_MOSI)
_bus = displayio.FourWire(_spi, command=LCD_DC, chip_select=LCD_CS, reset=LCD_RST)
DISPLAY = adafruit_displayio_ssd1306.SSD1306(_bus, width=128, height=64)

