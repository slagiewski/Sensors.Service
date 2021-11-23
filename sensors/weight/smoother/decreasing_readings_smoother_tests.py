from re import T
import statistics
from datetime import datetime

from decreasing_reading_smoother import DecreasingReadingSmoother

Object = lambda **kwargs: type("Object", (), kwargs)

def reading_below_radius_should_be_skipped():
    readings = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    expected_mean = statistics.fmean(readings)

    def save_reading(reading):
        return (datetime.now().strftime("%d/%m/%Y_%H:%M:%S"), reading)

    repo = Object(
        get_latest_readings=lambda take: readings,
        save_new_reading=save_reading 
    )

    smoother = DecreasingReadingSmoother(repo, smoothing_radius=2)
    result = smoother.smooth(10)

    assert result == expected_mean

def no_historic_readings_should_return_current_value():
    repo_save_called = False

    def save_reading():
        repo_save_called = True

    repo = Object(
        get_latest_readings=lambda take: [],
        save_new_reading=save_reading
    )

    smoother = DecreasingReadingSmoother(repo, smoothing_radius=2)

    expected_result = 2.5
    result = smoother.smooth(current_reading=expected_result)

    assert repo_save_called
    assert result == expected_result


reading_below_radius_should_be_skipped()
no_historic_readings_should_return_current_value()