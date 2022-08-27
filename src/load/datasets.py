import numpy as np
import pandas as pd
from typing import Tuple
from src.models.ubs import UBS
from src.models.city import City
from src.models.state import State
from sqlalchemy.orm import Session


def update_alter_city_id(session: Session, base_path: str) -> Tuple[bool, str]:
    try:
        # Carrega dataset para processamento e inicia controle de status
        codes = pd.read_csv(f"{base_path}/data/Codigo_Nome_Municipios.txt", sep=";", encoding = "latin1")
        progress = 0

        # Acessa dados de estados, para recuperar identificação do IBGE
        states = session.query(State.ibge_state_id, State.id).all()
        def search(code: int):
            relation_code = 0
            for state in states:
                if state.ibge_state_id == code:
                    relation_code = state.id
            return relation_code

        # Prepara a execução de atualização
        for i in range(0, len(codes)):
            # Recupera informações da carga
            token = City.tokenize(codes["NOME MUNICIPIO"].values[i])
            state_code = int(str(codes["CODIGO MUNICIPIO"].values[i])[:2])

            session.query(City).filter_by(token=token, state_id=search(state_code)).update({
                "data_city_id": codes["CODIGO MUNICIPIO"].values[i]
            })

            # Exibe status do progresso
            progress = round((i + 1) * 100 / len(codes), 2)
            print(f"Progresso de atualização de ID alternativo para cidade: {progress}%", end="\r")

        print("\nFinalizada atualização de IDs alternativos para cidades.")
        return True, ""

    except BaseException as e:
        return False, str(e)


def update_city_geo(session: Session, base_path: str) -> Tuple[bool, str]:
    try:
        # Carrega dataset para processamento e inicia controle de status
        geos = pd.read_csv(f"{base_path}/data/Sedes_Coordenadas_Municipios.csv", sep=";")
        progress = 0

        # Prepara execução da atualização
        for i in range(0, len(geos)):
            alter_id = geos["CODIGO MUNICIPIO"].values[i]
            session.query(City).filter_by(data_city_id=alter_id).update({
                "latitude": geos["LATITUDE"].values[i],
                "longitude": geos["LONGITUDE"].values[i]
            })

            # Exibe status do progresso
            progress = round((i + 1) * 100 / len(geos), 2)
            print(f"Progresso de atualização de coordenadas para cidades: {progress}%", end="\r")

        print("\nFinalizado processo de carga de coordenadas geográficas dos centros das cidades.")
        return True, ""

    except BaseException as e:
        return False, str(e)


def update_city_pib(session: Session, base_path: str) -> Tuple[bool, str]:
    try:
        # Carrega base de processamento e inicia controle de status
        pibs = pd.read_excel(f"{base_path}/data/PIB_Municipios.xls", sheet_name="PIB_dos_Municípios")
        pibs = pibs.query(f"Ano == 2019")
        progress = 0

        for i in range(0, len(pibs)):
            ibge_code = pibs["Código do Município"].values[i]
            session.query(City).filter_by(ibge_city_id=ibge_code).update({
                "pib_billion": pibs["Produto Interno Bruto, \na preços correntes\n(R$ 1.000)"].values[i] / 1000000
            })

            # Exibe status do progresso
            progress = round((i + 1) * 100 / len(pibs), 2)
            print(f"Progresso de atualização do PIB das cidades: {progress}%", end="\r")

        print("\nFinalizado processo de carga de PIB das cidades.")
        return True, ""

    except BaseException as e:
        return False, str(e)


def update_city_population(session: Session, base_path: str) -> Tuple[bool, str]:
    try:
        # Carrega base de processamento e inicia controle de status
        population = pd.read_excel(f"{base_path}/data/POP2021_20220711.xls", sheet_name="Municípios", dtype={
            "COD. MUNIC": str, "COD. UF": str
        })
        progress = 0

        for i in range(0, len(population)):
            ibge_code = population["COD. UF"].values[i] + population["COD. MUNIC"].values[i]
            city_pop = population["POPULAÇÃO ESTIMADA"].values[i]
            session.query(City).filter_by(ibge_city_id=ibge_code).update({
                "population": city_pop if type(city_pop) != str else int(city_pop.split("(")[0].replace(".", ""))
            })

            # Exibe status do progresso
            progress = round((i + 1) * 100 / len(population), 2)
            print(f"Progresso de atualização de população estimada para cidades: {progress}%", end="\r")

        print("\nFinalizado processo de carga de população estimada das cidades.")
        return True, ""

    except BaseException as e:
        return False, str(e)


def update_city_area(session: Session, base_path: str) -> Tuple[bool, str]:
    try:
        # Carrega bases de processamento e inicia controle de progresso
        areas = pd.read_excel(f"{base_path}/data/Areas_Municipios.xls", sheet_name="AR_BR_MUN_2021")
        progress = 0

        for i in range(0, len(areas)):
            ibge_code = areas["CD_MUN"].values[i]
            session.query(City).filter_by(ibge_city_id=ibge_code).update({
                "area": areas["AR_MUN_2021"].values[i]
            })

            # Exibe status do progresso
            progress = round((i + 1) * 100 / len(areas), 2)
            print(f"Progresso de atualização da área de cidades: {progress}%", end="\r")

        print("\nFinalizado processo de carga de área das cidades.")
        return True, ""

    except BaseException as e:
        return False, str(e)


def load_ubs(session: Session, base_path: str) -> Tuple[bool, str]:
    try:
        # Carrega bases para processamento e controle do progresso
        ubs = pd.read_csv(f"{base_path}/data/cadastro_estabelecimentos_cnes.csv", sep=";", dtype={"CNES": str})
        cities = session.query(City.data_city_id, City.id).all()
        progress = 0
        skip = 0
        add = []

        # Define a busca de registro pelo id alternativo
        def search(alter_id: int):
            code = 0
            for city in cities:
                if city.data_city_id == alter_id:
                    code = city.id
                    break
            return code

        for i in range(0, len(ubs)):
            alter_code = ubs["IBGE"].values[i]
            city_id = search(alter_code)

            # Garante que valores vazios sejam inseridos
            lat, long = ubs["LATITUDE"].values[i], ubs["LONGITUDE"].values[i]
            lat = None if np.isnan(lat) else lat
            long = None if np.isnan(long) else long

            # Garante que todos os ids alternativos estejam carregados
            if city_id == 0:
                skip = skip + 1
                continue

            add.append(UBS(
                cnes=ubs["CNES"].values[i],
                city_id=city_id,
                latitude=lat,
                longitude=long
            ))

            # Exibe status do progresso
            progress = round((i + 1) * 100 / len(ubs), 2)
            print(f"Progresso da carga de UBS: {progress}%", end="\r")

        print(f"\nFinalizado processo de adição de UBS com um total de {skip} skips.")
        session.add_all(add)
        return True, ""

    except BaseException as e:
        return False, str(e)
