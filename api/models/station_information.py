from sqlalchemy import Column, Integer, JSON, String, UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import insert
import uuid

Base = declarative_base()


class StationInformation(Base):
    __tablename__ = 'stations_information'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    station_id = Column(String, unique=True)
    lon = Column(Integer)
    lat = Column(Integer)
    rental_uris = Column(JSON)
    _bcycle_station_type = Column(String)
    address = Column(String)
    name = Column(String)

    @classmethod
    def upsert_stations_information(cls, session, data):
        stmt = insert(StationInformation).values(data)
        stmt = stmt.on_conflict_do_update(constraint='stations_information_station_id_key', set_={
            "lon": stmt.excluded.lon,
            "lat": stmt.excluded.lat,
            "rental_uris": stmt.excluded.rental_uris,
            "_bcycle_station_type": stmt.excluded._bcycle_station_type,
            "address": stmt.excluded.address,
            "name": stmt.excluded.name
        })
        session.execute(stmt)
        return True