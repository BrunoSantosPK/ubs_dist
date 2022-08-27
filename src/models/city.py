import re
import unicodedata
from src.models.base import Base
from nltk.stem import RSLPStemmer
from sqlalchemy import Column, Integer, String, ForeignKey, Float


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    name = Column(String(50), nullable=False)
    token = Column(String(50), nullable=True)
    ibge_city_id = Column(Integer, nullable=False)
    data_city_id = Column(Integer, nullable=True)
    population = Column(Integer, nullable=True)
    pib_billion = Column(Float, nullable=True)
    area = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    @staticmethod
    def tokenize(text: str) -> str:
        text = re.sub("[^a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]", " ", text).lower()
        text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("ASCII")
        st = RSLPStemmer()
        return " ".join([st.stem(t) for t in text.split(" ") if t != ""])
