from w1thermsensor import W1ThermSensor, Sensor


def read_current_temperature():
    result = {}
    for sensor in W1ThermSensor.get_available_sensors([Sensor.DS18B20]):
        result[sensor.id] = sensor.get_temperature()
    return result

