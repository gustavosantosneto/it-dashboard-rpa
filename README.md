# it-dashboard-rpa

Projeto em Python que realiza a coleta de dados de forma automática

## Pacotes Python necessários: 

    dotenv_values
    pandas
    rpaframework
    xlsxwriter

## Variáveis de ambiente do arquivo .env

    AGENCIES_SPENDING_URL = "https://www.itdashboard.gov/itportfoliodashboard"
    AGENCY_INVESTMENTS_URL = "https://www.itdashboard.gov/search-advanced"
    AGENCIES_SHEET_NAME="Agências"
    TEST_AGENCY_NAME = "NATIONAL SCIENCE FOUNDATION"
    OUTPUT_PATH = "./output/"
    BUSINESS_CASES_DOWNLOAD_PATH = "./test_agency_business_cases/"
    LOG_PATH = "./log/"

## Sequência de passos para utilizar o projeto

    Instalar / Ter o Python 3.7+

    Instalar / Ter o navegador Chrome

    Executar o comando pip install -r dependencies.txt --upgrade

    Executar o arquivo Python main.py

## Observações

    O arquivo .ENV está exposto por motivo de não haver informações críticas como senhas
    Se tivesse mais tempo o que eu faria:
     - Organizaria os logs detalhando melhor cada momento e separando os arquivos .log por nível (info, erro)
     - Formatar o arquivo xlsx ajustando o tamanho das colunas
     - Fazer o download dos investment business case corretamente, pois ficou inacabado