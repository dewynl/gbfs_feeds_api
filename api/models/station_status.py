from sqlalchemy import Column, Integer, String, JSON, Boolean, UUID, MetaData, Table, select
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import insert
import uuid

Base = declarative_base()

class StationStatus(Base):
    __tablename__ = 'stations_status'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    station_id = Column(String, unique=True)
    is_returning = Column(Boolean)
    is_renting = Column(Boolean)
    is_installed = Column(Boolean)
    num_docks_available = Column(Integer)
    num_bikes_available = Column(Integer)
    last_reported = Column(Integer)
    num_bikes_available_types = Column(JSON)

    @classmethod
    def upsert_stations_status(cls, session, data):
        stmt = insert(StationStatus).values(data)
        stmt = stmt.on_conflict_do_update(constraint="stations_status_station_id_key", set_={
            "is_returning": stmt.excluded.is_returning,
            "is_renting": stmt.excluded.is_renting,
            "is_installed": stmt.excluded.is_installed,
            "num_docks_available": stmt.excluded.num_docks_available,
            "num_bikes_available": stmt.excluded.num_bikes_available,
            "last_reported": stmt.excluded.last_reported,
            "num_bikes_available_types": stmt.excluded.num_bikes_available_types
        })
        proxy =  session.execute(stmt)
        return proxy
    
    @classmethod
    def get_station_status(cls, db_engine, id):
        connection = db_engine.connect()
        metadata = MetaData()
        stations_status_table = Table(cls.__tablename__, metadata, autoload_replace=True, autoload_with=db_engine)

        query = select(stations_status_table.c.is_returning, 
                       stations_status_table.c.is_renting, 
                       stations_status_table.c.is_installed,
                       stations_status_table.c.num_docks_available,
                       stations_status_table.c.num_bikes_available,
                       stations_status_table.c.last_reported
                    ).where(stations_status_table.c.station_id == id)
        
        result = connection.execute(query).fetchone()
        result = result._asdict() if result else None
        return result