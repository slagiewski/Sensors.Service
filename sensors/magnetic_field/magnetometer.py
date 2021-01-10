from . import QMC5883L
import threading
import time
from datetime import datetime


class Payload():
    def __init__(self, keepgoing, last_changed: datetime, base_value, change_resolution, previous_value):
        self.keepgoing = keepgoing
        self.last_changed = last_changed
        self.base_value = base_value
        self.change_resolution = change_resolution
        self.previous_value = previous_value


payload = None
sensor = QMC5883L.QMC5883L()


def get_magnetic_field_value():
    magnetic_field = sensor.get_magnet()
    print("Current magnetic field: ", magnetic_field, datetime.utcnow())
    return magnetic_field


def get_last_value_changed_to_base_date():
    if not payload:
        raise "Init was not called!"
    return payload.last_changed


def init_value_changed_to_base_job(base_value, change_resolution_sec):
    print("Initiating magnetic field change job", datetime.utcnow())
    payload = Payload(
        keepgoing=True, last_changed=datetime.min, base_value=base_value, change_resolution=change_resolution_sec, previous_value=[-999, -999, -999])
    t = threading.Thread(
        target=__update_value_changed_to_base__, args=(payload,))
    t.start()
    return t


def __update_value_changed_to_base__(data: Payload):
    while data.keepgoing:
        print(f"\n[[Magnetic field check - {datetime.utcnow()}]]")
        time.sleep(1)
        current_value = sensor.get_magnet()
        print("Magnetic field: ", current_value)
        if (not __is_within_resolution__(data.last_changed, data.change_resolution) and
                not __is_value_close_to_previous_value__(data.previous_value, current_value) and
                __is_value_close_to_base__(data.base_value, current_value)):
            print("\tMagnetic field value changed to base value: ", datetime.utcnow())
            data.last_changed = datetime.utcnow()
        data.previous_value = current_value


def __is_value_close_to_previous_value__(previous_value, current_value):
    result = __are_values_close__(previous_value, current_value)
    print("Current value is close to previous value: ", result)
    return result


def __is_value_close_to_base__(base_value, current_value):
    result = __are_values_close__(base_value, current_value)
    print("Is magnetic field value close to base: ", result)
    return result


def __are_values_close__(base_value, current_value):
    x_offset = abs(current_value[0] - base_value[0])
    y_offset = abs(current_value[1] - base_value[1])

    result = x_offset < 200 and y_offset < 200

    return result


def __is_within_resolution__(last_checked_date, resolution_sec):
    result = abs(datetime.utcnow() -
              last_checked_date).total_seconds() < resolution_sec
    print("Is within resolution: (result, now, last, res) ", result, datetime.utcnow(), last_checked_date, resolution_sec)
    return result
