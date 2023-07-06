import sys
from signalrcore.hub_connection_builder import HubConnectionBuilder
import logging
import requests
import json
import time
import os
import psycopg2


class Main:
    def __init__(self):
        self._hub_connection = None
        self.HOST = os.getenv('HOST')  # Setup your host here
        self.TOKEN = os.getenv('TOKEN')  # Setup your token here
        self.TICKS = os.getenv('TICKS')  # Setup your TICKS here
        self.T_MAX = os.getenv('T_MAX')  # Setup your max temperature here
        self.T_MIN = os.getenv('T_MIN')  # Setup your min temperature here
        self.DB_HOST = os.getenv('DB_HOST')  # Setup your database here
        self.DB_NAME = os.getenv('DB_NAME')  # Setup your database here
        self.DB_USER = os.getenv('DB_USER')  # Setup your database here
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')  # Setup your database here
        self.DB_PORT = os.getenv('DB_PORT')  # Setup your database here

    def __del__(self):
        if self._hub_connection != None:
            self._hub_connection.stop()

    def setup(self):
        self.setSensorHub()

    def start(self):
        self.setup()
        self._hub_connection.start()

        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

    def setSensorHub(self):
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )

        self._hub_connection.on("ReceiveSensorData", self.onSensorDataReceived)
        self._hub_connection.on_open(lambda: print("||| Connection opened."))
        self._hub_connection.on_close(lambda: print("||| Connection closed."))
        self._hub_connection.on_error(lambda data: print(f"||| An exception was thrown closed: {data.error}"))

    def onSensorDataReceived(self, data):
        try:
            date = data[0]["date"]
            dp = float(data[0]["data"])
            self._send_event_to_database(date, "DataReceived")
            #  self.send_temperature_to_fastapi(date, dp)
            self.analyzeDatapoint(date, dp)
        except Exception as err:
            print(err)

    def analyzeDatapoint(self, date, data):
        if float(data) >= float(self.T_MAX):
            self.sendActionToHvac(date, "TurnOnAc", self.TICKS)
        elif float(data) <= float(self.T_MIN):
            self.sendActionToHvac(date, "TurnOnHeater", self.TICKS)

    def sendActionToHvac(self, date, action, nbTick):
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{nbTick}")
        details = json.loads(r.text)
        self._send_event_to_database(date, action)
        print(details)

    def _send_event_to_database(self, timestamp, event):
        try:
            conn = psycopg2.connect(
                f"host={self.DB_HOST}\
                  port={self.DB_PORT}\
                  dbname={self.DB_NAME}\
                  user={self.DB_USER}\
                  password={self.DB_PASSWORD}"
            )
            curr = conn.cursor()

            curr.execute('SELECT count(*) FROM oxygencs.event_log;')
            count_before = curr.fetchone()[0]

            curr.execute(
                'INSERT INTO oxygencs.event_log(created_at, event) VALUES (%s, %s);',
                (timestamp, event)
            )
            conn.commit()

            curr.execute('SELECT count(*) FROM oxygencs.event_log;')
            count_after = curr.fetchone()[0]

            if count_after == count_before:
                raise psycopg2.DataError("Event was not inserted.")
            else:
                print(f"Event '{event}' was inserted.")

        except (psycopg2.Error, psycopg2.DataError) as e:
            print(f"An error occured while trying to save an event ({event}). {e}", file=sys.stderr)
        finally:
            curr.close()
            conn.close()


if __name__ == "__main__":
    main = Main()
    main.start()
