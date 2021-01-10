#!/usr/bin/env python

import flask
from flask import request, jsonify

from sensors.weight import weight_sensor
from sensors.temperature import temperature_sensor

from config import sensors

APP = flask.Flask(__name__)

ROOT_PATH = "/sensors"


@APP.route(f"{ROOT_PATH}/weight")
def weight():
    weight_scale_config = sensors["weight_scale"]
    result = weight_sensor.read_grams(
        weight_scale_config["output_pin"], weight_scale_config["pd_sck_pin"])
    return jsonify({"weight": result})


@APP.route(f"{ROOT_PATH}/temperature")
def temperature():
    result = temperature_sensor.read_current_temperature()
    return jsonify({"sensors": result})


if __name__ == '__main__':
    APP.debug = True
    APP.run(host='0.0.0.0')
