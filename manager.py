import sys
import nltk
import requests
from typing import Tuple
from dotenv import load_dotenv
from src.models.base import Base
from src.models.city import City
from src.models.state import State
from sqlalchemy.orm import Session
from src.database.connection import get_engine, get_session


def create_database():
    try:
        nltk.download("rslp", quiet=True)
        Base.metadata.create_all(get_engine())
        print("Tabelas criadas com sucesso!")

    except BaseException as e:
        print(str(e))


def delete():
    try:
        Base.metadata.drop_all(get_engine())
        print("Tabelas removidas do banco de dados.")

    except BaseException as e:
        print(e)


def seed():
    try:
        # inicia conexão e chama os seeds especializados
        session = get_session()
        success, message = seed_states(session)
        if not success: raise Exception(message)

        success, message = seed_cities(session)
        if not success: raise Exception(message)

        # Executa as mudanças
        session.commit()
        print("Seed realizado com sucesso, seus dados foram carregados!")
        
    except BaseException as e:
        print(str(e))
        session.rollback()

    finally:
        session.close()


def seed_states(session: Session) -> Tuple[bool, str]:
    try:
        # Acessa dados de estados a partir da API do IBGE
        url = "http://servicodados.ibge.gov.br/api/v1/localidades/estados"
        req = requests.get(url)
        data = req.json()

        # Cria a lista para inserção
        states = []
        for reg in data:
            states.append(State(
                symbol=reg["sigla"],
                name=reg["nome"],
                ibge_state_id=reg["id"],
                region=reg["regiao"]["sigla"]
            ))

        # Envia para adição
        session.add_all(states)
        return True, ""
    
    except BaseException as e:
        return False, str(e)


def seed_cities(session: Session) -> Tuple[bool, str]:
    try:
        # Acessa estados para recuperar id IBGE e executar busca na API
        states = session.query(State.ibge_state_id, State.id).all()
        cities = []

        for state in states:
            url = f"http://servicodados.ibge.gov.br/api/v1/localidades/estados/{state.ibge_state_id}/municipios"
            req = requests.get(url)
            data = req.json()

            # Adiciona um novo município para cadastro
            for reg in data:
                cities.append(City(
                    state_id=state.id,
                    name=reg["nome"],
                    ibge_city_id=reg["id"],
                    token=City.tokenize(reg["nome"])
                ))
        
        # Envia para adição
        session.add_all(cities)
        return True, ""

    except BaseException as e:
        return False, str(e)


if __name__ == "__main__":
    args = sys.argv
    load_dotenv("config/.env")
    globals()[args[1]]()
