import rp2040_stamp_photolight_board as board
from adafruit_debouncer import Debouncer
import digitalio
import neopixel

#from adafruit_led_animation.animation.blink import Blink
#from adafruit_led_animation.animation.sparklepulse import SparklePulse
#from adafruit_led_animation.animation.comet import Comet
#from adafruit_led_animation.animation.chase import Chase
#from adafruit_led_animation.animation.pulse import Pulse
#from adafruit_led_animation.animation.sparkle import Sparkle
#from adafruit_led_animation.animation.rainbowchase import RainbowChase
#from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
#from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.solid import Solid
#from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.rainbow import Rainbow
#from adafruit_led_animation.animation.customcolorchase import CustomColorChase
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import (
    WHITE,
    RED,
    GREEN,
    BLUE,
    CYAN,
    PURPLE,
    YELLOW,
)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 16, brightness=0.2, auto_write=False)

animations = AnimationSequence(
    Solid(pixels, color=WHITE),
    Solid(pixels, color=RED),
    Solid(pixels, color=GREEN),
    Solid(pixels, color=BLUE),
    Solid(pixels, color=CYAN),
    Solid(pixels, color=PURPLE),
    Solid(pixels, color=YELLOW),
    Rainbow(pixels, speed=0.1, period=5),
)

io_left = digitalio.DigitalInOut(board.SW_LEFT)
io_left.switch_to_input(pull=digitalio.Pull.UP)
left = Debouncer(io_left)

io_right = digitalio.DigitalInOut(board.SW_RIGHT)
io_right.switch_to_input(pull=digitalio.Pull.UP)
right = Debouncer(io_right)

io_center = digitalio.DigitalInOut(board.SW_CENTER)
io_center.switch_to_input(pull=digitalio.Pull.UP)
center = Debouncer(io_center)

while True:
    left.update()
    right.update()
    center.update()

    animations.animate()

    if left.fell:
        idx = animations._current - 1
        animations.activate(idx % len(animations._members))
    elif right.fell:
        animations.next()
    elif center.fell:
        b = pixels.brightness + 0.2
        if b > 1.0:
            b = 0.2
        pixels.brightness = b
