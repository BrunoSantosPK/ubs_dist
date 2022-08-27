# Alocação de unidades básicas de saúde no território nacional
*A ideia deste repositório é criar uma sistematização da distruição de unidades de saúde ao longo do Brasil, para que seja fonte de estudo e correlaçoes.*

## Ambiente
Para compor este projeto, é importante possuir o Python instalado na máquina. A execução pode ser feita por meio de ambiente virtual, instalando dependências pelo "pip install -r requirements.txt". Feito isto, qualquer IDE conseguirá interagir com este repositório.

## Ferramentas
Desenvolvido com a versão 3.10.4 do Python em um sistema operacional Ubuntu 22.04 e utilizando VS Code como editor de texto. Algumas ferramentas importantes foram:

- Jupyter
- SQL Alchemy
- MySQL
- Pandas e Numpy
- NLTK
- Matplotlib

## Arquivos
Os dados trabalhados neste repositório foram obtidos a partir da plataforma de dados do governo federal ([aqui](https://dados.gov.br/)), pelo portal de acesso à informação e o site oficial do IBGE. Por fins de organização, alguns arquivos foram renomeados, para facilitar a codificação. Os dados base de localidade foram obtidos por meio da API do IBGE ([aqui](https://servicodados.ibge.gov.br/api/docs/localidades)).

|Arquivo|Local|Acesso|
|---|---|---|
|cadastro_estabelecimentos_cnes.csv|[link](https://dados.gov.br/dataset/unidades-basicas-de-saude-ubs)|13/08/2022|
|Codigo_Nome_Municipios.txt|[link](http://www.consultaesic.cgu.gov.br/busca/dados/Lists/Pedido/Item/displayifs.aspx?List=0c839f31%2D47d7%2D4485%2Dab65%2Dab0cee9cf8fe&ID=1012693&Web=88cc5f44%2D8cfe%2D4964%2D8ff4%2D376b5ebb3bef)|14/08/2022|
|Sedes_Coordenadas_Municipios.csv|[link](http://www.consultaesic.cgu.gov.br/busca/dados/Lists/Pedido/Item/displayifs.aspx?List=0c839f31%2D47d7%2D4485%2Dab65%2Dab0cee9cf8fe&ID=1012693&Web=88cc5f44%2D8cfe%2D4964%2D8ff4%2D376b5ebb3bef)|14/08/2022|
|POP2021_20220711.xls|[link](https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html?=&t=resultados)|15/08/2022|
|PIB_Municipios.xls|[link](https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9088-produto-interno-bruto-dos-municipios.html?=&t=downloads)|15/08/2022|
|Areas_Municipios.xls|[link](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/15761-areas-dos-municipios.html?=&t=acesso-ao-produto)|22/08/2022|

## Carga
O banco de dados foi inicializado e preenchido por meio dos modelos declarativos do SQLAlchemy. Isso gera ganho na possibilidade de manipular os dados utilizando notações de OO, deixando o código mais organizado e de alto nível.

Uma dificuldade foi o descompasso entre os IDs de municípios no arquivo de cadastro de UBS, que apresentam uma diferença para os IDs utilizados pelo IBGE. Assim, fica como alternativa fazer a busca pelo nome da cidade. Para superar o desafio de diversas possibilidades de escrita de nome nas diversas bases utilizadas, o model para cidades carrega um método estático que implementa uma normalização (avaliando radicais das palavras), que será utilizada para comparar os nomes de forma segura.

O processo de carga foi implementado no arquivo manager.py, criado de modo a ser utilizado via terminal (as regras de transformação estão no módulo **load**). Esta carga tem como objetivo inicializar as tabelas no banco de dados, carregar informações padrão da API do IGBE e transformar os dados obtidos pelos arquivos na seção "Arquivos". Seguem os comandos disponíveis:

- `python manager.py delete` : remove todas as tabelas do banco de dados.
- `python manager.py create_database` : faz a criação das tabelas no banco de dados.
- `python manager.py seed` : executa o seed (cadastro) de dados padrão nas tabelas.
- `python manager.py feature_engineering` : carrega os dados dos arquivos utilizados, aplicando regras de negócio.
- `python manager.py pipeline` : executa o processo de reset e carga todal de informações, sendo útil em cargas iniciais.

OBS.: O manager.py está configurado para lançar uma exceção sempre que um comando não válido for informado.

## Status
Projeto em andamento: repositório e registro de informações finalizado.