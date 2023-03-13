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