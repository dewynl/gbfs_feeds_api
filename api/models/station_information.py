from sqlalchemy import Column, Integer, JSON, String, UUID
from sqlalchemy.orm import declarative_base
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