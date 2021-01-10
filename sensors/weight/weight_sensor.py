import RPi.GPIO as GPIO
import time
import sys
from .hx711 import HX711

# Force Python 3 ###########################################################

if sys.version_info[0] != 3:
    raise Exception("Python 3 is required.")

############################################################################


offset = 8386889.0625
ratio = -8.079287234042553


def __clean__():
    print("Cleaning...")
    GPIO.cleanup()


def __get_amplifier__(output_pin, pd_sck_pin):
    hx = HX711(output_pin, pd_sck_pin)
    hx.set_offset(offset=offset)
    hx.set_scale(ratio)
    return hx


def __reset_chip__(hx: HX711):
    hx.power_down()
    time.sleep(.001)
    hx.power_up()


def read_grams(output_pin, pd_sck_pin):
    hx = __get_amplifier__(
        output_pin, pd_sck_pin)

    try:
        result = hx.get_grams(32)
        __reset_chip__(hx)
        return result
    except (SystemExit):
        __clean__()
