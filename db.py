import psycopg
import time

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


