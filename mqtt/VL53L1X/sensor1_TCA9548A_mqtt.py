import time
import board
import adafruit_vl53l1x
import adafruit_tca9548a
import paho.mqtt.client as paho

global count_blocked_1
global count_blocked_2

count_blocked_1 = 0
count_blocked_2 = 0

broker="test.mosquitto.org"

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

sensor_client= paho.Client("sensor1")                           #create client object
sensor_client.on_publish = on_publish                          #assign function to callback
sensor_client.connect(broker)

# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

# For each sensor, create it using the TCA9548A channel instead of the I2C object
vl53_1 = adafruit_vl53l1x.VL53L1X(tca[1])
vl53_2 = adafruit_vl53l1x.VL53L1X(tca[2])

# OPTIONAL: can set non-default values
vl53_1.distance_mode = 2
vl53_2.distance_mode = 2
vl53_1.timing_budget = 33
vl53_2.timing_budget = 33

vl53_1.start_ranging()
vl53_2.start_ranging()

# Real: width between two sensors: 110cm, width of two people: 90cm
guideline = 70
max_difference = 30
threshold = 2

# Demo
# guideline = 15
# max_difference = 30
# threshold = 1

# After initial setup, can just use sensors as normal.
# for i in range(1, 100):
#     print(vl53_1.distance, vl53_2.distance)
#     time.sleep(0.1)

def main():
    count_blocked_1 = 0
    count_blocked_2 = 0

    while True:
        if vl53_1.data_ready:
            if vl53_1.distance is not None and vl53_1.distance < guideline:
                count_blocked_1 += 1

        if vl53_2.data_ready:
            if vl53_2.distance is not None and vl53_2.distance < guideline:
                count_blocked_2 += 1

        if (count_blocked_1 > threshold): # Input
            sensor_client.publish("embed/control", "2 " + str(vl53_1.distance))
            print("Send %s" % str(vl53_1.distance))
            print("2, ", count_blocked_1)
            count_blocked_1 = 0
            count_blocked_2 = 0
            time.sleep(0.3)

        elif (count_blocked_2 > threshold): # Output
            sensor_client.publish("embed/control", "3 " + str(vl53_2.distance))
            print("Send %s" % str(vl53_2.distance))
            print("3, ", count_blocked_2)
            count_blocked_1 = 0
            count_blocked_2 = 0
            time.sleep(0.3)

        vl53_1.clear_interrupt()
        vl53_2.clear_interrupt()
        time.sleep(0.025)

if (__name__ == '__main__'):
    main()