import RPi.GPIO as GPIO
import time
import sys
import statistics
from .hx711 import HX711


def __clean__():
    print("Cleaning...")
    GPIO.cleanup()


def __get_amplifier__(output_pin, pd_sck_pin, offset, ratio):
    hx = HX711(output_pin, pd_sck_pin)
    hx.set_offset(offset=offset)
    hx.set_scale(ratio)
    return hx


def __reset_chip__(hx: HX711):
    hx.power_down()
    time.sleep(.01)
    hx.power_up()


def read_grams(output_pin, pd_sck_pin, weight_offset, weight_ratio):
    hx = __get_amplifier__(
        output_pin, pd_sck_pin, offset=weight_offset, ratio=weight_ratio)

    try:
        result = statistics.median([hx.get_grams(16) for i in range(4)])
        __reset_chip__(hx)
        return result
    except (SystemExit):
        __clean__()
