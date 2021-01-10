from . import QMC5883L

sensor = QMC5883L.QMC5883L()

while True:
    m = sensor.get_magnet()
    print(m)
