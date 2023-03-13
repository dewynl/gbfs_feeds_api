from sqlalchemy import MetaData, Table, Column, UUID, String, Boolean, Integer, JSON
from models.station_status import StationStatus
from models.station_information import StationInformation


def create_tables(engine):
    metadata = MetaData()

    Table(StationStatus.__tablename__, metadata, 
        Column('id', UUID(as_uuid=True), primary_key=True),
        Column('station_id', String, unique=True),
        Column('is_returning', Boolean),
        Column('is_renting', Boolean),
        Column('is_installed', Boolean),
        Column('num_docks_available', Integer),
        Column('num_bikes_available', Integer),
        Column('last_reported', Integer),
        Column('num_bikes_available_types', JSON)
    )

    Table(StationInformation.__tablename__, metadata,
          Column('id', UUID(as_uuid=True), primary_key=True),
          Column('station_id', String, unique=True),
          Column('lon', Integer),
          Column('lat', Integer),
          Column('rental_uris', JSON),
          Column('_bcycle_station_type', String),
          Column('address', String),
          Column('name', String)
    )

    metadata.create_all(engine)