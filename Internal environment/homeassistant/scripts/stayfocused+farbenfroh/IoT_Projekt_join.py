#import of all needed packages
import json
#import requests
import time
import datetime
#import urllib
#import logging
import homeassistant.remote as remote
import configparser
import ast
from TelegramBotSkript import TelegramBot
from farbenfroh import FarbenFroh


lastLectureValue = "off"
breakAlert = 0
lastrun = datetime.datetime.now().replace(hour=0, minute= 0)
fake_update = {'ok': True, 'result': [{'update_id': 0, 'message': {'message_id': 765, 'from': {'id': 0, 'first_name': 'J', 'language_code': 'de-DE'}, 'text': '', 'chat': {'type': 'private', 'id': 0, 'first_name': 'J'}, 'date': 1497357549, 'entities': [{'offset': 0, 'type': 'bot_command', 'length': 6}]}}]}

#Config
Config = configparser.ConfigParser()
Config.read("/home/homeassistant/.homeassistant/scripts/stayfocused+farbenfroh/config.ini")
#logging.basicConfig(format='%(asctime)s;%(message)s', datefmt='%Y.%m.%d;%H:%M:%S', level=logging.INFO, filename='sensor.csv')

#Connect to Home Assistant
api = remote.API(Config.get('HomeAssistant', 'IP'), Config.get('HomeAssistant', 'PW'))

#Global Variable
goodRoom = True
            
#Default values
values = {'temp_min': False, 'temp_max': False, 'temp_bright': 0, 'hum_min': False, 'hum_max': False, 'hum_bright': 0, 'Co2_max': False, 'Co2_bright': 0, 'light_min': False, 'light_bright': 0}
tempAvg = float(22.0)
humAvg = float(50.0)
Co2Avg = float(600.0)
lightAvg = float(600.0)

farbenFroh = FarbenFroh()
telegramBot = TelegramBot()

#logger setup
#logger = logging.getLogger('myapp')
#hdlr = logging.FileHandler('/home/homeassistant/.homeassistant/logs/TelegramBot.log')
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#hdlr.setFormatter(formatter)
#logger.addHandler(hdlr)
#logger.setLevel(logging.INFO)

def checkHAStatus():
    #check if lecture status has changed, send update to telegram bot so it can react accordingly
    global lastLectureValue, breakAlert
    textlist = []
    lectureValue = remote.get_state(api, "input_boolean.breakrequest").state
    if lectureValue == lastLectureValue:
        pass
    else:
        if lectureValue == "on":
            lastLectureValue = lectureValue
            breakAlert = 0
            textlist.append('lectureStart')
        else:
            lastLectureValue = lectureValue
            textlist.append('lectureStop')
    #check if break score has exceeded limit, send update to telegram bot so it can notify users
    breakScore = int(remote.get_state(api, "sensor.breakscore").state)
    if breakScore < 100:
        breakAlert = 0
        pass
    elif breakScore > 100 and breakScore <150:
        if breakAlert == 0:
            breakAlert = 1
            textlist.append('breakAlert')
    else:
        if breakAlert == 1:
            breakAlert = 2
            textlist.append('breakAlert')
        else:
            pass
    return textlist

def toggle_button(info):
    #toggles the button in the home assistant interface
    #used to request breaks and turn lecture on and off
    if info == "lectureOn":
        remote.call_service(api, 'input_boolean', 'turn_on', {'entity_id': '{}'.format('input_boolean.stopwatch')})
    elif info == "lectureOff":
        remote.call_service(api, 'input_boolean', 'turn_off', {'entity_id': '{}'.format('input_boolean.stopwatch')})
    elif info == "breakRequest":
        remote.call_service(api, 'input_boolean', 'toggle', {'entity_id': '{}'.format('input_boolean.breakrequest')})

#main function - contains an infinite loop
#gets all new updates from telegram since the last update processed by this script
#calls the function handle updates to react to telegram updates
#then handles any possible status changes in home assistant (lecture turned on/off, limits for break/air quality/brightness crossed)
def main():
    global tempAvg, humAvg, Co2Avg, lightAvg, fake_update, lastrun, api
    last_update_id = None
    response1 = None
    while True:
        #print('started loop')
        try:
            temp = remote.get_state(api, Config.get('Sensors', 'Temp')).state
            if temp != 'unknown':
                tempAvg = float(temp)
            hum = remote.get_state(api, Config.get('Sensors', 'Hum')).state
            if hum != 'unknown':
                humAvg = float(hum)
            Co2 = remote.get_state(api, Config.get('Sensors', 'Co2')).state
            if Co2 != 'unknown':
                Co2Avg = float(Co2)
            light = remote.get_state(api, Config.get('Sensors', 'Light')).state
            if light != 'unknown':
                lightAvg = float(light)
            #print(tempAvg, humAvg, Co2Avg, lightAvg)
        except Exception as e:
            #print("Getting states: "+str(e))
            pass
        try:
            updates = telegramBot.get_updates(last_update_id)
            if len(updates["result"]) > 0:
                last_update_id = telegramBot.get_last_update_id(updates) + 1
                infolist = telegramBot.handle_updates(updates)
                for info in infolist:
                    toggle_button(info)
                time.sleep(1)
        except Exception as e:
            #print("Telegram Msgs: "+str(e))
            pass
        try:
            currentrun = datetime.datetime.now()
            check = currentrun - lastrun
            if lastrun < currentrun and check > datetime.timedelta(minutes=2):
                #print("running FarbenFroh")
                textlist = farbenFroh.changeLightColor(Config, values, api, tempAvg, humAvg, Co2Avg, lightAvg)
                #print(textlist)
                for text in textlist:
                    fake_update['result'][0]['message']['text'] = text
                    telegramBot.handle_updates(fake_update)
                lastrun = datetime.datetime.now()
            else:
                #print("not running FarbenFroh this loop")
                pass
        except Exception as e:
            #print("Change Color: "+str(e))
            pass
        try:
            textlist = checkHAStatus()
            for text in textlist:
                    fake_update['result'][0]['message']['text'] = text
                    telegramBot.handle_updates(fake_update)
        except Exception as e:
            #print("Send status to TG: "+str(e))
            pass

#executes main function upon start of python script
if __name__ == '__main__':
    main()
