import sys
from typing import Tuple
import requests
from dotenv import load_dotenv
from src.models.base import Base
from src.database.connection import get_engine, get_session
from sqlalchemy.orm import Session
from src.models.state import State
from src.models.city import City


def create_database():
    try:
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


if __name__ == "__main__":
    args = sys.argv
    load_dotenv("config/.env")
    globals()[args[1]]()
