import time
import math
from datetime import datetime, timedelta, UTC
from fmiopendata.wfs import download_stored_query
from db import Database

db = Database()

TOPICS = {
    "weather": {
        "Air temperature": 301,
        "Relative humidity": 302,
        "Pressure (msl)": 303,
        "Wind speed": 304,
        "Wind direction": 305,
        "Gust speed": 306,
        "Dew-point temperature": 307,
        "Precipitation amount": 308,
        "Horizontal visibility": 309,
    },
    "mareograph": {
        "Water stemperature": 300,
    },
    "wave": {
        "Water temperature": 300,
    },
}

STATIONS = [
    {"id": 101794, "station_type": "weather"},
    {"id": 101786, "station_type": "weather"},
    {"id": 134248, "station_type": "mareograph"},
    {"id": 103807, "station_type": "wave"},
]

QUERY_IDS = {
    "weather": "fmi::observations::weather::multipointcoverage",
    "mareograph": "fmi::observations::mareograph::multipointcoverage",
    "wave": "fmi::observations::wave::multipointcoverage",
}

def fetch_station(fmisid, station_type):

    end = datetime.now(UTC)
    start = end - timedelta(hours=2)

    start_str = start.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_str = end.strftime("%Y-%m-%dT%H:%M:%SZ")

    obs = download_stored_query(
        QUERY_IDS[station_type],
        args=[
            f"fmisid={fmisid}",
            f"starttime={start_str}",
            f"endtime={end_str}",
        ],
    )

    timestamp = next(iter(obs.data))

    # print(timestamp)
    print(obs.data[timestamp])
    return obs

# parse data and save to database
def save_data(obs, fmisid, station_type):

    mapping = TOPICS[station_type]

    for timestamp, stations in obs.data.items():

        station_data = next(iter(stations.values()))

        for field_name, topic_id in mapping.items():

            field = station_data.get(field_name)
            if field is None:
                continue

            value = field["value"]

            if math.isnan(value):
                continue

            # print(
            #     fmisid,
            #     topic_id,
            #     timestamp,
            #     float(value),
            # )

            db.insert_weather_observation(fmisid, topic_id, timestamp, float(value))
        db.commit()

def main():

    while True:
        for station in STATIONS:
            try:
                data = fetch_station(station["id"], station["station_type"])
                save_data(data, station["id"], station["station_type"])
            except Exception as e:
                print(e)

        time.sleep(3600)

if __name__ == "__main__":
    main()
