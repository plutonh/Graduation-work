import paho.mqtt.client as paho
import time

available_people = 0
guideline = 80
threshold = 1
sensor_state = [0, 0, 0, 0]

global input_lock
global output_lock

input_lock = 0
output_lock = 0

##FIXME: Do not close the gate when there is a person!!


def handle_change(mqtt_client, change):
    global available_people
    if change == 1:
        if available_people == 0:
            # Open the gate
            mqtt_client.publish('embed/motor', "1")
            print("send 1 to motor, open")
        available_people += 1
    elif change < 0:
        prev_num_people = available_people
        available_people += change

        if prev_num_people > 0 and available_people <= 0:
            # Close the gate
            mqtt_client.publish('embed/motor', "0")
            print("send 0 to motor, close")
    
    mqtt_client.publish('embed/web', str(available_people))
    print("send %d to the website" % available_people)

def increase_people(mqtt_client):
    # The payload between two sensors is 20 cm 
    # The detected length = 20 cm - sensor_state[0] - sensor_state[1]
    # Let's conclude there are two people when the length > 12cm 
    # sensor_state[0] + sensor_state[1] < 8 cm
    if sensor_state[0] + sensor_state[2] < guideline:
        # Two people
        print("Two person IN")
        handle_change(mqtt_client, 2)
    else:
        # One people
        print("One person IN")
        handle_change(mqtt_client, 1)

    sensor_state[0] = 0
    sensor_state[1] = 0
    sensor_state[2] = 0
    sensor_state[3] = 0

    print("increase")

def decrease_people(mqtt_client):
    # The payload between two sensors is 20 cm 
    # The detected length = 20 cm - sensor_state[0] - sensor_state[1]
    # Let's conclude there are two people when the length > 12cm 
    # sensor_state[0] + sensor_state[1] < 8 cm
    if sensor_state[1] + sensor_state[3] < guideline:
        # Two people
        print("Two people OUT")
        handle_change(mqtt_client, -2)
    else:
        # One person
        print("One person OUT")
        handle_change(mqtt_client, -1)

    sensor_state[0] = 0
    sensor_state[1] = 0
    sensor_state[2] = 0
    sensor_state[3] = 0

    print("decrease")  

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def on_message(client, userdata, msg):
    global input_lock
    global output_lock

    publisher_id, data = msg.payload.decode("utf-8").split(' ')
    publisher_id = int(publisher_id)

    print(publisher_id)

    if publisher_id == 0 or publisher_id == 2: # Input
        if publisher_id == 0:
            data_0 = float(data)
            sensor_state[publisher_id] = data_0
        else:
            data_2 = float(data)
            sensor_state[publisher_id] = data_2
        
        #  print("increase, ", sensor_state[0], " and ", sensor_state[2])
        if sensor_state[0] != 0 and sensor_state[2] != 0:
            increase_people(client)

    elif publisher_id == 1 or publisher_id == 3: # Output
        if publisher_id == 1:
            data_1 = float(data)
            sensor_state[publisher_id] = data_1
        else:
            data_3 = float(data)
            sensor_state[publisher_id] = data_3

        # print("decrease, ", sensor_state[1], " and ", sensor_state[3])
        if sensor_state[1] != 0 and sensor_state[3] != 0:
            decrease_people(client)
    
    elif publisher_id == 4: # 2 -> 4 for additional sensors
        data = int(data)
        print("%s from the web" % data)
        handle_change(client, data)

mqtt_client = paho.Client()
mqtt_client.on_subscribe = on_subscribe
mqtt_client.on_publish = on_publish
mqtt_client.on_message = on_message
mqtt_client.connect('test.mosquitto.org')
mqtt_client.subscribe("embed/control", qos=1)

mqtt_client.loop_forever()



# import paho.mqtt.client as paho
# import time

# available_people = 0
# guideline = 20
# threshold = 1
# sensor_state = [0, 0, 0, 0]

# global input_lock
# global output_lock
# input_lock = 0
# output_lock = 0

# ##FIXME: Do not close the gate when there is a person!!


# def handle_change(mqtt_client, change):
#     global available_people
#     if change == 1:
#         if available_people == 0:
#             # Open the gate
#             mqtt_client.publish('embed/motor', "1")
#             print("send 1 to motor, open")
#         available_people += 1
#     elif change < 0:
#         prev_num_people = available_people
#         available_people += change

#         if prev_num_people > 0 and available_people <= 0:
#             # Close the gate
#             mqtt_client.publish('embed/motor', "0")
#             print("send 0 to motor, close")
    
#     mqtt_client.publish('embed/web', str(available_people))
#     print("send %d to the website" % available_people)

# def increase_people(mqtt_client):
#     if sensor_state[0] != 0 and sensor_state[2] != 0:
#         # The payload between two sensors is 20 cm 
#         # The detected length = 20 cm - sensor_state[0] - sensor_state[1]
#         # Let's conclude there are two people when the length > 12cm 
#         # sensor_state[0] + sensor_state[1] < 8 cm
#         if sensor_state[0] + sensor_state[2] < guideline:
#             # Two people
#             print("Two people IN")
#             handle_change(mqtt_client, +2)
#         else:
#             # One people
#             print("One people IN")
#             handle_change(mqtt_client, +1)

#         sensor_state[0] = 0
#         sensor_state[1] = 0
#         sensor_state[2] = 0
#         sensor_state[3] = 0

#         print("increase")

# def decrease_people(mqtt_client):
#     if sensor_state[1] != 0 and sensor_state[3] != 0:
#         # The payload between two sensors is 20 cm 
#         # The detected length = 20 cm - sensor_state[0] - sensor_state[1]
#         # Let's conclude there are two people when the length > 12cm 
#         # sensor_state[0] + sensor_state[1] < 8 cm
#         if sensor_state[1] + sensor_state[3] < guideline:
#             # Two people
#             print("Two people OUT")
#             handle_change(mqtt_client, -2)
#         else:
#             # One people
#             print("One people OUT")
#             handle_change(mqtt_client, -1)

#         sensor_state[0] = 0
#         sensor_state[1] = 0
#         sensor_state[2] = 0
#         sensor_state[3] = 0

#         print("decrease")  

# def on_subscribe(client, userdata, mid, granted_qos):
#     print("Subscribed: "+str(mid)+" "+str(granted_qos))

# def on_publish(client,userdata,result):             #create function for callback
#     print("data published \n")
#     pass

# def on_message(client, userdata, msg):
#     global input_lock
#     global output_lock

#     publisher_id, data = msg.payload.decode("utf-8").split(' ')
#     publisher_id = int(publisher_id)

#     print(publisher_id)

#     if publisher_id == 0 or publisher_id == 2:
#         if output_lock > 0:
#             output_lock -= 1
#             sensor_state[0] = 0
#             sensor_state[2] = 0
#         else:
#             if publisher_id == 0:
#                 data_0 = float(data)
#                 sensor_state[publisher_id] = data_0
#             else:
#                 data_2 = float(data)
#                 sensor_state[publisher_id] = data_2
#             increase_people(client)
#             input_lock = threshold

#     elif publisher_id == 1 or publisher_id == 3:
#         if input_lock > 0:
#             input_lock -= 1
#             sensor_state[1] = 0
#             sensor_state[3] = 0
#         else:
#             if publisher_id == 1:
#                 data_1 = float(data)
#                 sensor_state[publisher_id] = data_1
#             else:
#                 data_3 = float(data)
#                 sensor_state[publisher_id] = data_3
#             decrease_people(client)
#             output_lock = threshold
    
#     elif publisher_id == 4: # 2 -> 4 for additional sensors
#         data = int(data)
#         print("%s from the web" % data)
#         handle_change(client, data)

# mqtt_client = paho.Client()
# mqtt_client.on_subscribe = on_subscribe
# mqtt_client.on_publish = on_publish
# mqtt_client.on_message = on_message
# mqtt_client.connect('test.mosquitto.org')
# mqtt_client.subscribe("embed/control", qos=1)

# mqtt_client.loop_forever()