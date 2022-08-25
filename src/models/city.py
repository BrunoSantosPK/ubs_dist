from src.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    name = Column(String(50), nullable=False)
