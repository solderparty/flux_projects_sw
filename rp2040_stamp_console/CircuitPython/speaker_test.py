import time
import array
import math
import rp2040_stamp_console_board as board
import digitalio
from audiocore import RawSample
from adafruit_waveform import square

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

button = digitalio.DigitalInOut(board.BTN_A)
button.switch_to_input(pull=digitalio.Pull.UP)

spk_n = digitalio.DigitalInOut(board.SPK_N)
spk_n.switch_to_output()
spk_n.value = False

tone_volume = 1
#frequency = 540  # Set this to the Hz of the tone you want to generate.
#length = 8000 // frequency

#sine_wave = array.array("H", [0] * length)
#for i in range(length):
#    sine_wave[i] = int((1 + math.sin(math.pi * 2 * i / length)) * (2 ** 15 - 1))

sine_wave = square.square_wave(14)
for i in range(len(sine_wave)):
    sine_wave[i] = int(sine_wave[i] * tone_volume)

audio = AudioOut(board.SPK_P)
sine_wave_sample = RawSample(sine_wave)

print(sine_wave)

while True:
    if not button.value:
        audio.play(sine_wave_sample, loop=True)
        time.sleep(0.25)
        audio.stop()
