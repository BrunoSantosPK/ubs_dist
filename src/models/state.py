from src.models.base import Base
from sqlalchemy import Column, Integer, String


class State(Base):
    __tablename__ = "states"
    id = Column(Integer, primary_key=True)
    symbol = Column(String(2), nullable=False)
    name = Column(String(20), nullable=False)
    ibge_state_id = Column(Integer, nullable=False)
    region = Column(String(2), nullable=True)
