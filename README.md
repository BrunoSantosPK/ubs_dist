# Alocação de unidades básicas de saúde no território nacional
*A ideia deste repositório é criar uma sistematização da distruição de unidades de saúde ao longo do Brasil, para que seja fonte de estudo e correlaçoes.*

# Ambiente
Para compor este projeto, é importante possuir o Python instalado na máquina. As dependências deste projeto podem ser totalmente obtidas por meio de um ambiente virtual, instaladas por meio do comando "pip install -r requirements.txt". Feito isto, qualquer IDE conseguirá interagir com este repositório.

# Arquivos
Os dados trabalhados aqui foram obtidos a partir da plataforma de dados do governo federal ([aqui](https://dados.gov.br/)), pelo portal de acesso à informação e o site oficial do IBGE. Os nomes foram mantidos como na origem e abaixo seguem os detalhes de download.

|Arquivo|Local|Acesso|
|---|---|---|
|cadastro_estabelecimentos_cnes.csv|[link](https://dados.gov.br/dataset/unidades-basicas-de-saude-ubs)|13/08/2022|
|Codigo_Nome_Municipios.txt|[link](http://www.consultaesic.cgu.gov.br/busca/dados/Lists/Pedido/Item/displayifs.aspx?List=0c839f31%2D47d7%2D4485%2Dab65%2Dab0cee9cf8fe&ID=1012693&Web=88cc5f44%2D8cfe%2D4964%2D8ff4%2D376b5ebb3bef)|14/08/2022|
|Sedes_Coordenadas_Municipios.csv|[link](http://www.consultaesic.cgu.gov.br/busca/dados/Lists/Pedido/Item/displayifs.aspx?List=0c839f31%2D47d7%2D4485%2Dab65%2Dab0cee9cf8fe&ID=1012693&Web=88cc5f44%2D8cfe%2D4964%2D8ff4%2D376b5ebb3bef)|14/08/2022|
|POP2021_20220711.xls|[link](https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html?=&t=resultados)|15/08/2022|
|PIB dos Municбpios - base de dados 2010-2019.xls|[link](https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9088-produto-interno-bruto-dos-municipios.html?=&t=downloads)|15/08/2022|
|AR_BR_RG_UF_RGINT_RGIM_MES_MIC_MUN_2021.xls|[link](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/15761-areas-dos-municipios.html?=&t=acesso-ao-produto)|22/08/2022|

OBS.: Importante reservar um espaço para pontuar sobre datas. Tanto os dados das UBS quanto os de população são de 2021, mais recentes nas plataformas oficiais. Todavia, não está disponível o PIB por estado para 2021 oficialmente na plataforma do IBGI, sendo 2019 o dado mais recente.

# Status
Projeto em andamento: repositório e registro de informações finalizado.