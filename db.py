import psycopg
import time

class Database:
    def __init__(self):
        while True:
            try:
                self.conn = psycopg.connect(
                    host="postgres-v2",
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
            ON CONFLICT (station_id, topic_id, timestamp)
            DO UPDATE SET value = EXCLUDED.value
            """,
            (station_id, topic_id, timestamp, value),
        )

    def insert_weather_observation(self, station_id, topic_id, timestamp, value):
        self.cur.execute(
            """
            INSERT INTO weather_observations
            (station_id, topic_id, timestamp, value)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (station_id, topic_id, timestamp)
            DO UPDATE SET value = EXCLUDED.value
            """,
            (station_id, topic_id, timestamp, value),
        )

    def commit(self):
        self.conn.commit()

