import RPi.GPIO as GPIO
from .historic_readings import weight_readings_repository as weight_repository
import time
import sys
import statistics

from .smoother import decreasing_reading_smoother as DecreasingReadingSmoother
from .hx711 import HX711

def read_grams(output_pin, pd_sck_pin, weight_offset, weight_ratio, withSmoothing: bool) -> float:
    current_value = __read_grams__(output_pin, pd_sck_pin, weight_offset, weight_ratio)
    
    if not withSmoothing:
        return current_value

    return __smooth_decreasing_reading__(current_value)

    

def __smooth_decreasing_reading__(current_reading: float) -> float:
    smoother = DecreasingReadingSmoother(repo=weight_repository, smoothing_radius=25)
    return smoother.smooth(current_reading)


def __read_grams__(output_pin, pd_sck_pin, weight_offset, weight_ratio) -> float:
    hx = __get_amplifier__(
        output_pin, pd_sck_pin, offset=weight_offset, ratio=weight_ratio)

    try:
        result = statistics.median([hx.get_grams(16) for i in range(4)])
        __reset_chip__(hx)
        return result
    except (SystemExit):
        __clean__()

    
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