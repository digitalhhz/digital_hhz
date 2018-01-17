#!/usr/bin/python


# EDIT: September 18, 2017
# DESCRIPTION 
# As part of an one-year project at Herman Hollerith Zentrum (HHZ),
# an IoT environment was set up. 
# 
# ADDITIONAL INFORMATION
# - Used sensor: REHAU air quality sensor
# - See: http://kuehnast.com/s9y/archives/641-Luftqualitaet-im-Innenraum-Air-Quality-Sensor-am-Raspberry-Pi.html
# - Modified by manh3141 


# Import required modules
import os
import time
import paho.mqtt.client as mqtt


# Define credentials and connection details of MQTT broker
user = "USER"
passwd = "PASSWORD"
mqttbroker = "XXX.XXX.X.XX"
channel = "CHANNEL"

# Define path of the airsensor-script and command to be executed
dir = "PATH"
cmd = dir + " -v -o"

# Execute airsensor-script to get air quality value
valAirQ = ""
p = os.popen(cmd,"r")

while 1:
    # Save air quality value to a variable
    valAirQ = p.readline()
    if not valAirQ: break
    valAirQ = valAirQ.replace("\n", "")    

    # Send air quality value to MQTT broker
    def on_connect(client, userdata, flags, rc):
      print("Connected with result code " + str(rc))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.username_pw_set(user, passwd)
    client.connect(mqttbroker, 1883, 60)
    client.publish(channel, valAirQ)

