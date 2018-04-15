import configparser
import logging
import requests
import sqlite3

#Config
Config = configparser.ConfigParser()
Config.read("config.ini")
logging.basicConfig(format='%(asctime)s;%(message)s', datefmt='%Y.%m.%d;%H:%M:%S', level=logging.INFO, filename='sensor.csv')

def dbConnect():
    conn = sqlite3.connect('home-assistant_v2.db')
    c = conn.cursor()
    return c;

def getTables(sensor, room):
    c = dbConnect();
    query = 'SELECT * FROM states where entity_id="' + sensor + '" ORDER BY last_updated DESC LIMIT 1;';
    for row in c.execute(query):
        post(getData(row, room))

def getData(result, room):
    print(result)
    return {
        'state_id': result[0],
        'domain': result[1],
        'entity_id': result[2],
        'state': result[3],
        'attributes': result[4],
        'event_id': result[5],
        'last_changed': result[6],
        'last_updated': result[7],
        'created': result[8],
        'location': room,
        'pass': Config.get('Extern', 'PW')}

def post(payload):
    r = requests.post(Config.get('Extern', 'IP'), data=payload)
    if(r.text!='true'):
        logging.info(r.text)

rooms = Config.items('Sensors')
for key, room in rooms:
    sensors = Config.items(room)
    for index, sensor in sensors:
        getTables('sensor.' + sensor, key)


