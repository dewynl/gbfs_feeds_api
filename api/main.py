import os, json
import urllib.request
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction

from models.station_information import StationInformation
from models.station_status import StationStatus
from utils.create_tables import create_tables

DB_URI = os.environ['DATABASE_URL'].replace("postgresql://", "cockroachdb://")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

def ingest_data(session, data):
    feeds = data['feeds']
    station_status_url = [i for i in feeds if i['name'] == 'station_status']
    station_information_url = [i for i in feeds if i['name'] == 'station_information']

    if len(station_status_url) == 0 or len(station_status_url) == 0:
        # Handle error if there is not station_status.
        return None
    
    station_status_url = station_status_url.pop()['url']
    station_information_url = station_information_url.pop()['url']

    try:
        station_status_response = urllib.request.urlopen(station_status_url).read()
        station_status_response_json = json.loads(station_status_response)
        stations_status = station_status_response_json['data']['stations']

        stations_information_response = urllib.request.urlopen(station_information_url).read()
        stations_information_response_json = json.loads(stations_information_response)
        stations_information = stations_information_response_json['data']['stations']


        StationStatus.upsert_stations_status(session, stations_status)
        StationInformation.upsert_stations_information(session, stations_information)

    except Exception as e:
        print(str(e))

@app.route('/ingest', methods = ['POST'])
def ingest():
    data = request.get_json().get('data', {}).get('en', {})
    run_transaction(sessionmaker(bind=engine), lambda s: ingest_data(s, data))
    return data


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8001))
    try:
        engine = create_engine(DB_URI, connect_args={"application_name":"gbfs_api"})
        create_tables(engine)
    except Exception as e:
        print("Failed to connect to database.")
        print(f"{e}")
        raise e


    app.run(debug=True, host='0.0.0.0', port=port)