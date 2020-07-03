
import paho.mqtt.client as mqtt
import pygame
import pyautogui as pgi

pygame.init()
# pygame.mouse.set_visible(True)
# pygame.display.set_mode((800,600),0,32)
pgi.FAILSAFE = False
pgi.PAUSE = 0.1

# MQTT cfg
mqtt_user = "magicSpace"
mqtt_pass = "magicspace"
mqtt_topics = ["magicSpaceMouseX", "magicSpaceMouseY", "magicSpaceMouse"]
mqtt_broker_ip = "192.168.0.105"

#active_mouse_pos = pygame.mouse.get_pos()
active_mouse_x = 0
active_mouse_y = 0
mouse_status = "UP"

client = mqtt.Client()
# Setup MQTT client
client.username_pw_set(mqtt_user, mqtt_pass)


def log(msg):
    if True:
        print(msg)


# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    log("Connected!" + str(rc))

    # Once the client has connected to the broker, to subscribe the topic
    for topic in mqtt_topics:
        client.subscribe(topic)
    # subscribe.client("magicSpaceMouseX")
    # client.subscribe("magicSpaceMouseX")


def on_message(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
    #mg = int.from_bytes(msg.payload)
    global active_mouse_x
    global active_mouse_y
    global mouse_status
    log("Topic: " + msg.topic + "\nMessage: " + str(int(msg.payload)))

    if msg.topic == "magicSpaceMouseX":
        active_mouse_x = int(msg.payload)
        log("mousing to: " + str(active_mouse_x) + ", " + str(active_mouse_y))
        pgi.moveTo(active_mouse_x, None, 0.001)
        #pygame.mouse.set_pos(active_mouse_x, active_mouse_y)
    elif msg.topic == "magicSpaceMouseY":
        active_mouse_y = int(msg.payload)
        log("mousing to: " + str(active_mouse_x) + ", " + str(active_mouse_y))
        pgi.moveTo(None, active_mouse_y, 0.001)
        #pygame.mouse.set_pos(active_mouse_x, active_mouse_y)
    elif msg.topic == "magicSpaceMouse":
        mouse_status = int(msg.payload)
        if mouse_status == 1:
            log("clicking mouse @: " + str(active_mouse_x) +
                ", " + str(active_mouse_y))
            pgi.mouseDown()

        elif mouse_status == 0:
            log("releasing mouse @: " + str(active_mouse_x) +
                ", " + str(active_mouse_y))
            pgi.mouseUp()

    # pygame.mouse.set_visible(True)

    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata


# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
client.on_connect = on_connect
client.on_message = on_message

# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using
client.connect(mqtt_broker_ip, 1883)

# Once we have told the client to connect, let the client object run itself
client.loop_forever()
client.disconnect()
