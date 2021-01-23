#!/usr/bin/env python

import flask
from flask import request, jsonify

from sensors.weight import weight_sensor
from sensors.temperature import temperature_sensor
#from sensors.magnetic_field import magnetometer

from config import sensors

APP = flask.Flask(__name__)

ROOT_PATH = "/sensors"

job_handles = []


@APP.route(f"{ROOT_PATH}/weight")
def weight():
    weight_scale_config = sensors["weight_scale"]
    result = weight_sensor.read_grams(
        weight_scale_config["output_pin"], weight_scale_config["pd_sck_pin"], weight_scale_config["offset"], weight_scale_config["ratio"])
    return jsonify({"weight": result})


@APP.route(f"{ROOT_PATH}/temperature")
def temperature():
    result = temperature_sensor.read_current_temperature()
    return jsonify({"sensors": result})


@APP.route(f"{ROOT_PATH}/magnetic_field")
def magnetic_field():
    result = magnetometer.get_magnetic_field_value()
    return jsonify({"X": result[0], "Y": result[1]})


@APP.route(f"{ROOT_PATH}/magnetic_field/last_changed")
def magnetic_field_last_changed():
    result = magnetometer.get_last_value_changed_to_base_date()
    return jsonify({"last_changed": result})


def __init_magnetometer_job__():
    magnetometer_config = sensors["magnetometer"]
    magnetometer.init_value_changed_to_base_job(
        magnetometer_config["base_value"], magnetometer_config["change_resolution_sec"])


def main():
    #    job_handles.append(__init_magnetometer_job__())
    APP.debug = True
    APP.run(host='0.0.0.0')


if __name__ == '__main__':
    main()
