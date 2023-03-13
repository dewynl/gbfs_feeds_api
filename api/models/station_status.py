from sqlalchemy import Column, Integer, String, JSON, Boolean, UUID
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