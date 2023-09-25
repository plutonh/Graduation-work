import VL53L1X
import RPi.GPIO as GPIO
import time

XSHUT1 = 8
XSHUT2 = 7

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(XSHUT1, GPIO.OUT)
GPIO.setup(XSHUT2, GPIO.OUT)
GPIO.output(XSHUT1, False)
GPIO.output(XSHUT2, False)

for count in range(1, 20):
    GPIO.output(XSHUT1, True)

    tof1 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
    tof1.open()
    tof1.start_ranging(1)
    distance = tof1.get_distance()
    tof1.stop_ranging()
    print("sensor 1: ",distance)
    tof1.change_address(new_address = 0x28)

    tof1.open()

    GPIO.output(XSHUT2, True)

    tof2 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x28)
    tof2.open()
    tof2.start_ranging(1)
    distance = tof2.get_distance()
    tof2.stop_ranging()
    print("sensor 2: ",distance)
    tof2.change_address(new_address = 0x29)

    tof2.open()
