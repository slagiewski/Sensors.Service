#!/usr/bin/env python

import flask
from flask import request, jsonify

from sensors.weight import weight_sensor
from sensors.temperature import temperature_sensor

from config import sensors as sensors_config

APP = flask.Flask(__name__)

ROOT_PATH = "/sensors"


@APP.route(f"{ROOT_PATH}/weight")
def weight():
    weight_scale_config = sensors_config["weight_scale"]

    withSmoothing = request.args.get('smoothing', default = False, type = bool)

    result = weight_sensor.read_grams(
        weight_scale_config["output_pin"], weight_scale_config["pd_sck_pin"], weight_scale_config["offset"], weight_scale_config["ratio"],
        withSmoothing)
    return jsonify({"weight": result})


@APP.route(f"{ROOT_PATH}/temperature")
def temperature():
    result = temperature_sensor.read_current_temperature()
    return jsonify({"sensors": result})

def main():
    APP.debug = True
    APP.run(host='0.0.0.0')


if __name__ == '__main__':
    main()
