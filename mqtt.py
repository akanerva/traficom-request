from paho.mqtt import client as mqtt
import logging
import json
import psycopg
import time
from datetime import datetime, UTC

class Database:
    def __init__(self):
        while True:
            try:
                self.conn = psycopg.connect(
                    host="postgres",
                    dbname="weather",
                    user="weather",
                    password="mypassword",
                )
                break
            except psycopg.OperationalError:
                print("Waiting for PostgreSQL...")
                time.sleep(2)
        self.cur = self.conn.cursor()

    def insert_measurement(self, station_id, topic_id, timestamp, value):
        self.cur.execute(
            """
            INSERT INTO measurements
            (station_id, topic_id, timestamp, value)
            VALUES (%s, %s, %s, %s)
            """,
            (station_id, topic_id, timestamp, value),
        )
        self.conn.commit()

stations = {
    "12001": "vt4_Oulu_Ouluntulli",
    "12017": "vt8_Liminka_Lapinkangas",
    "12022": "vt4_Liminka_Haaransilta",
    "12033": "vt22_Muhos_Kosulankylä",
    "12053": "Liminka-Tupos",
}

topics = {
    "22": "SADE",
    "23": "SADE_INTENSITEETTI",
    "24": "SADESUMMA",
    "25": "SATEEN_OLOMUOTO_PWDXX",
    "26": "NÄKYVYYS_KM",
    "176": "KITKA_1",
    "177": "VEDEN_MÄÄRÄ_1",
    "181": "KITKA1_LUKU",
    "186": "KITKA_2",
    "187": "VEDEN_MÄÄRÄ_2",
    "191": "KITKA2_LUKU",
}

def on_connect(client, userdata, flags, reason_code, properties=None):

    print(f"Connected (reason_code={reason_code})")

    mqtt_topics = [
        (f"weather-v2/{station_id}/{topic_id}", 0)
        for station_id in stations
        for topic_id in topics
    ]

    mqtt_topics.append(("weather-v2/status", 0))

    client.subscribe(mqtt_topics)

def on_disconnect(client, userdata, flags, reason_code, properties=None):
    print(
        f"Disconnected:"
        f"\n  flags={flags}"
        f"\n  reason={reason_code}"
        f"\n  properties={properties}"
    )

def on_subscribe(client, userdata, mid, reason_codes, properties=None):
    print(f"Subscribed: mid={mid}, reason_codes={reason_codes}")

def on_message(client, userdata, msg):
    # print(msg.topic, msg.payload.decode())
    parse_message(msg)

def on_socket_open(client, userdata, sock):
    print("Socket opened")

def on_socket_close(client, userdata, sock):
    print("Socket closed")

def on_socket_register_write(client, userdata, sock):
    print("Socket register write")

def on_socket_unregister_write(client, userdata, sock):
    print("Socket unregister write")

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="kaleksi-test",
    transport="websockets"
)

def parse_message(msg):
    # jos status, poistu
    if "status" in msg.topic:
        return

    #[0] boilerplate, [1] asema, [2] topic
    message = msg.topic.split("/")
    station_id = message[1]
    topic_id = message[2]

    payload = msg.payload.decode("utf-8")
    data = json.loads(payload)

    value = data["value"]

    timestamp = data["time"]
    dt = datetime.fromtimestamp(timestamp, UTC)
    formatted = dt.strftime("%d-%m-%Y_%H:%M")
    line = f"{formatted},{stations[station_id]},{topics[topic_id]},{value}"
    print(line)
    db.insert_measurement(
        station_id,
        topic_id,
        dt,
        data["value"],
    )


logging.basicConfig(level=logging.DEBUG)

client.enable_logger()
db = Database()

# client.ws_set_options(path="/mqtt")
client.tls_set()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_socket_open = on_socket_open
client.on_socket_close = on_socket_close
client.on_socket_register_write = on_socket_register_write
client.on_socket_unregister_write = on_socket_unregister_write
client.connect("tie.digitraffic.fi", 443)
client.loop_forever()

