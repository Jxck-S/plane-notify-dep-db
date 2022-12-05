import requests
import csv
import time
import psycopg2
from psycopg2.extras import execute_values
import gzip
import json
import configparser
import pause
import datetime
import sys
conf = configparser.ConfigParser()
conf.read('conf.ini')
while True:
    conn = psycopg2.connect(
        database= conf['DATABASE']['DB'],
        user= conf['DATABASE']['USER'],
        password= conf['DATABASE']['PW'],
        host= conf['DATABASE']['HOST'],
        port= conf['DATABASE']['PORT']
    )
    table = 'our_airports_airports'
    conn.autocommit = False
    cursor = conn.cursor()
    print("Getting Ourairports airports")
    airport_content_csv = requests.get("https://davidmegginson.github.io/ourairports-data/airports.csv")
    airport_content_csv = airport_content_csv.content.decode('utf-8').splitlines()
    cursor.execute(f"DELETE FROM {table}")
    overrides = {'latitude_deg': 'lat', 'longitude_deg': 'lon', 'elevation_ft': 'elev'}
    for org_key, new_key in overrides.items():
        airport_content_csv[0] = airport_content_csv[0].replace(org_key, new_key)
    airport_csv = list(csv.DictReader(airport_content_csv))
    columns = airport_csv[0].keys()
    conversions = {"id": "int", "lat": "float", "lon": "float", "elev": "float"}
    for idx, airport in enumerate(airport_csv):
        for key, convert_to in conversions.items():
            if airport[key]:
                tp = float if convert_to == "float" else int
                airport_csv[idx][key] = tp(airport[key])
            else:
                airport_csv[idx][key] = None
    query = "INSERT INTO {} ({}) VALUES %s".format(table, ','.join(columns))
    values = [[value for value in row.values()] for row in airport_csv]
    execute_values(cursor, query, values)
    conn.commit()


    print("Getting Ourairports regions")
    table = 'our_airports_regions'
    airport_content_csv = requests.get("https://davidmegginson.github.io/ourairports-data/regions.csv")
    airport_content_csv = airport_content_csv.content.decode('utf-8').splitlines()
    cursor.execute(f"DELETE FROM {table}")
    overrides = {'latitude_deg': 'lat', 'longitude_deg': 'lon', 'elevation_ft': 'elev'}
    for org_key, new_key in overrides.items():
        airport_content_csv[0] = airport_content_csv[0].replace(org_key, new_key)
    airport_csv = list(csv.DictReader(airport_content_csv))
    columns = airport_csv[0].keys()
    conversions = {"id": "int"}
    for idx, airport in enumerate(airport_csv):
        for key, convert_to in conversions.items():
            if airport[key]:
                tp = float if convert_to == "float" else int
                airport_csv[idx][key] = tp(airport[key])
            else:
                airport_csv[idx][key] = None
    query = "INSERT INTO {} ({}) VALUES %s".format(table, ','.join(columns))
    values = [[value for value in row.values()] for row in airport_csv]
    execute_values(cursor, query, values)
    conn.commit()




    def get_adsbx_ac():
        r = requests.get("https://downloads.adsbexchange.com/downloads/basic-ac-db.json.gz", stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            gzip_file = gzip.GzipFile(fileobj=r.raw)
            ac = []
            t = gzip_file.read()
            t = t.decode('utf8')
            for row in t.splitlines():
                    jso = json.loads(row)
                    ac.append(jso)
            print(f"Got {len(ac)} aircraft from ADSBX")
            return ac
    table = 'adsbx_ac'

    cursor.execute(f"DELETE FROM {table}")

    print("Getting ADSBX AC")
    airport_csv = get_adsbx_ac()
    columns = airport_csv[0].keys()
    query = "INSERT INTO {} ({}) VALUES %s".format(table, ','.join(columns))
    values = [[value for value in row.values()] for row in airport_csv]
    execute_values(cursor, query, values)
    conn.commit()
    cursor.close()
    conn.close()

    today = datetime.date.today()
    t = datetime.time(2, 30)
    today_t = datetime.datetime.combine(today, t)
    week_from_now = today_t + datetime.timedelta(days=7)
    print("Pausing till", week_from_now.strftime("%Y-%m-%d %I:%M %p"))
    sys.stdout.flush()
    pause.until(week_from_now)