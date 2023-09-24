import VL53L1X
import RPi.GPIO as GPIO

XSHUT_1 = 8
XSHUT_2 = 7

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Setup GPIO for shutdown pins on each VL53L1X
GPIO.setup(XSHUT_1,GPIO.OUT)
GPIO.setup(XSHUT_2,GPIO.OUT)

# Set all shutdown pins low to turn off each VL53L1X
GPIO.output(XSHUT_1,GPIO.LOW)
GPIO.output(XSHUT_2,GPIO.LOW)

tof1 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof1.open()
#tof1.change_address(new_address = 0x2B)
#GPIO.setup(XSHUT,GPIO.IN)
tof2 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof2.open()
# now tof1 has address 0x2B and tof2 has address 0x29

running = True

for count in range(1, 101):
    GPIO.output(XSHUT_1,GPIO.HIGH)
    tof1.start_ranging(1)                   # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range
    distance_in_mm = tof1.get_distance()    # Grab the range in mm
    tof1.stop_ranging()                     # Stop ranging
    print("sendor 1: ", distance_in_mm)
    GPIO.output(XSHUT_1,GPIO.LOW)

    GPIO.output(XSHUT_2,GPIO.HIGH)
    tof2.start_ranging(1)                   # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range
    distance_in_mm = tof2.get_distance()    # Grab the range in mm
    tof2.stop_ranging()                     # Stop ranging
    print("sensor 2: ", distance_in_mm)
    GPIO.output(XSHUT_2,GPIO.LOW)
