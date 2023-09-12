from nextwheel import NextWheel
from datetime import datetime


if __name__ == "__main__":
    # websocket.enableTrace(True)  # Uncomment to print all received data
    nw = NextWheel("10.0.1.2")
    # nw.connect()

    # Set params for sensors
    ret = nw.set_sensors_params(adc_sampling_rate=120, imu_sampling_rate=120, accelerometer_precision=8,
                                gyrometer_precision=2000)

    print(f'set_sensors_params returned code: {ret.status_code} text: {ret.text}')

    # Read back params from sensors
    ret = nw.get_sensors_params()
    if ret.status_code == 200:
        print(f'get_sensors_params returned code: {ret.status_code} json:', ret.json())

    #nw.close()
