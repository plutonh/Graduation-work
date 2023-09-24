import VL53L1X
import RPi.GPIO as GPIO

XSHUT = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(XSHUT,GPIO.OUT)
GPIO.output(XSHUT,GPIO.LOW)

tof1 = VL53L1X.VL53L1X(i2c_bus=0, i2c_address=0x2B)
tof1.open()
#tof1.change_address(new_address = 0x2B)
GPIO.setup(XSHUT,GPIO.IN)
tof2 = VL53L1X.VL53L1X(i2c_bus=0, i2c_address=0x2B)
tof2.open()
# now tof1 has address 0x2B and tof2 has address 0x29

running = True

while running:
    tof1.start_ranging(1)                   # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range
    distance_in_mm = tof1.get_distance()    # Grab the range in mm
    tof1.stop_ranging()                     # Stop ranging
    print(distance_in_mm)

    tof2.start_ranging(1)                   # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range
    distance_in_mm = tof2.get_distance()    # Grab the range in mm
    tof2.stop_ranging()                     # Stop ranging
    print(distance_in_mm)