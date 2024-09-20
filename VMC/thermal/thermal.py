
import base64
import time

import adafruit_mlx90640
import board
import busio
from bell.avr.mqtt.client import MQTTModule
from bell.avr.mqtt.payloads import AvrThermalReadingPayload
from loguru import logger


class ThermalModule(MQTTModule):
    def __init__(self):
        super().__init__()
        
        logger.debug("Connecting to thermal camera...")

        i2c = busio.I2C(board.SCL, board.SDA)


        self.amg = adafruit_mlx90640.MLX90640(i2c)
        #print("MLX addr detected on I2C")
        #print([hex(i) for i in self.amg.serial_number])
        self.amg.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
        logger.success("Connected to thermal camera!")

    def request_thermal_reading(self) -> None:
        reading = bytearray(768)
        frame = [0] * 768

        stamp = time.monotonic()
        try:
            self.amg.getFrame(frame)
        except ValueError:
            # these happen, no biggie - retry
            return
        i=0
        for h in range(24):
            for w in range(32):
                pix = frame[h * 32 + w]
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
