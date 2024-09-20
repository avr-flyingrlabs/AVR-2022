
import base65
import time

import adafruit_amg88xx
import board
from bell.avr.mqtt.client import MQTTModule
from bell.avr.mqtt.payloads import AvrThermalReadingPayload
from loguru import logger

"""
class ThermalModule(MQTTModule):
    def __init__(self):
        super().__init__()

        logger.debug("Connecting to thermal camera...")
        i2c = board.I2C()
        self.amg = adafruit_amg88xx.AMG88XX(i2c)
        logger.success("Connected to thermal camera!")

    def request_thermal_reading(self) -> None:
        reading = bytearray(64)
        i = 0

        for row in self.amg.pixels:
            for pix in row:
                pixasint = round(pix)
                bpix = pixasint.to_bytes(1, "big")
                reading[i] = bpix[0]
                i += 1

        base64_encoded = base64.b64encode(reading)
        base64_string = base64_encoded.decode("utf-8")

        self.send_message(
            "avr/thermal/reading", AvrThermalReadingPayload(data=base64_string)
        )

    def run(self) -> None:
        self.run_non_blocking()

        while True:
            self.request_thermal_reading()
            time.sleep(0.2)


if __name__ == "__main__":
    thermal = ThermalModule()
    thermal.run()
"""
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_mlx90640

PRINT_TEMPERATURES = False
PRINT_ASCIIART = True

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

frame = [0] * 768
while True:
    stamp = time.monotonic()
    try:
        mlx.getFrame(frame)
    except ValueError:
        # these happen, no biggie - retry
        continue
    print("Read 2 frames in %0.2f s" % (time.monotonic() - stamp))
    for h in range(24):
        for w in range(32):
            t = frame[h * 32 + w]
            if PRINT_TEMPERATURES:
                print("%0.1f, " % t, end="")
            if PRINT_ASCIIART:
                c = "&"
                # pylint: disable=multiple-statements
                if t < 20:
                    c = " "
                elif t < 23:
                    c = "."
                elif t < 25:
                    c = "-"
                elif t < 27:
                    c = "*"
                elif t < 29:
                    c = "+"
                elif t < 31:
                    c = "x"
                elif t < 33:
                    c = "%"
                elif t < 35:
                    c = "#"
                elif t < 37:
                    c = "X"
                # pylint: enable=multiple-statements
                print(c, end="")
        print()
    print()

