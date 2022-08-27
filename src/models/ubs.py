from src.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float


class UBS(Base):
    __tablename__ = "ubs"
    id = Column(Integer, primary_key=True)
    cnes = Column(String(10), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
