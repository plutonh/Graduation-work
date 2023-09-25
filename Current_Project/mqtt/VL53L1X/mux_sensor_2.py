# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows using two TSL2491 light sensors attached to TCA9548A channels 0 and 1.
# Use with other I2C sensors would be similar.
import time
import board
import adafruit_vl53l1x
import adafruit_tca9548a

# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

# For each sensor, create it using the TCA9548A channel instead of the I2C object
vl53_1 = adafruit_vl53l1x.VL53L1X(tca[1])
vl53_2 = adafruit_vl53l1x.VL53L1X(tca[2])

vl53_1.distance_mode = 1
vl53_2.distance_mode = 1

vl53_1.timing_budget = 33
vl53_2.timing_budget = 33

vl53_1.start_ranging()
vl53_2.start_ranging()

# After initial setup, can just use sensors as normal.
for i in range(1, 100):
    print(vl53_1.distance, vl53_2.distance)
    time.sleep(0.1)
