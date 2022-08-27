import os
import sys
import nltk
from dotenv import load_dotenv
from src.models.base import Base
from src.load.ibge import add_cities, add_states
from src.database.connection import get_engine, get_session
from src.load.datasets import update_alter_city_id, update_city_geo,\
    update_city_population, update_city_pib, update_city_area, load_ubs


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
        nltk.download("rslp", quiet=True)
        print("Iniciando processo de carga inicial do banco de dados.")

        success, message = add_states(session)
        if not success: raise Exception(message)

        success, message = add_cities(session)
        if not success: raise Exception(message)

        # Executa as mudanças
        session.commit()
        print("O banco de dados foi preenchido com as informações base do IBGE!")
        
    except BaseException as e:
        print(str(e))
        session.rollback()

    finally:
        session.close()


def feature_engineering(base_path: str):
    try:
        # Inicia conexão e chama as funções de carga
        session = get_session()
        print("Iniciando processo de feature engineering.")

        success, message = update_alter_city_id(session, base_path)
        if not success: raise Exception(message)

        success, message = update_city_geo(session, base_path)
        if not success: raise Exception(message)

        success, message = update_city_population(session, base_path)
        if not success: raise Exception(message)

        success, message = update_city_pib(session, base_path)
        if not success: raise Exception(message)

        success, message = update_city_area(session, base_path)
        if not success: raise Exception(message)

        success, message = load_ubs(session, base_path)
        if not success: raise Exception(message)

        session.commit()
        print("Processo de feature engineering finalizado!")

    except BaseException as e:
        print(str(e))
        session.rollback()

    finally:
        session.close()


def pipeline(base_path: str):
    delete()
    create_database()
    seed()
    feature_engineering(base_path)


if __name__ == "__main__":
    # Define path do projeto e carrega variáveis de ambiente
    functions = ["delete", "create_database", "seed", "feature_engineering", "pipeline"]
    base_path = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(f"{base_path}/config/.env")

    # Faz a chamada da função passada como parâmetro
    args = sys.argv
    if len(args) != 2:
        raise Exception("Comando inválido, utilize sempre python manager.py <nome_da_funcao>.")

    if args[1] not in functions:
        raise Exception(f"Função não encontrada. Estão disponíveis: {', '.join(functions)}")

    if args[1] in ["pipeline", "feature_engineering"]:
        globals()[args[1]](base_path)
    else:
        globals()[args[1]]()
