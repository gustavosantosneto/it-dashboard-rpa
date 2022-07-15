from dotenv import dotenv_values
from RPA.Browser.Selenium import Selenium
import logger
import data_manipulation
import re
import math

ENV = dotenv_values(".env")
AGENCIES_SPENDING_URL = ENV["AGENCIES_SPENDING_URL"]
AGENCY_INVESTMENTS_URL = ENV["AGENCY_INVESTMENTS_URL"]
AGENCIES_SHEET_NAME = ENV["AGENCIES_SHEET_NAME"]
TEST_AGENCY_NAME = ENV["TEST_AGENCY_NAME"]
BUSINESS_CASES_DOWNLOAD_PATH = ENV["BUSINESS_CASES_DOWNLOAD_PATH"]
OUTPUT_PATH = ENV["OUTPUT_PATH"]

logger = logger.logger


def get_agencies_spendings(browser):

    # Lista de departamentos com cabeçalho
    agencies_spendings = [[
        "Agency name",
        "FY 2022 IT Spending",
        "Spending on Major Investments"]]

    # Abre driver na URL
    browser.go_to(AGENCIES_SPENDING_URL)

    # Aguarda carregar um elemento na página
    browser.wait_until_page_contains_element(
        "css:div.spending-overview > h2",
        10
    )

    # Captura a lista de departamentos sem a primeira opção de "todos"
    agency_list = browser.get_list_items("id:agency-select")[1:]

    if len(agency_list) == 1:
        raise Exception("Nenhum departamento encontrado")

    for agency in agency_list:

        agency_fieds = get_agency_data(browser, agency)

        agencies_spendings.append(agency_fieds)

    return agencies_spendings


def get_agency_data(browser, agency):

    agency_fieds = []

    # Seleciona o departamento
    browser.select_from_list_by_label("id:agency-select", agency)

    # Aguarda carregar os dados do departamento
    browser.wait_until_element_contains(
        "css:div.spending-overview > h3",
        agency.upper(),
        10
    )

    # Coloca os dados do departamento na lista
    agency_fieds.append(agency)
    agency_fieds.append(
        browser.get_text("css:div.it-spending > p > strong")
    )
    agency_fieds.append(
        browser.get_text("css:div.it-spending > p > strong")
    )

    return agency_fieds


def get_agency_spending(browser, agency_name):
    # Lista de departamentos com cabeçalho
    agency_spendings = [[
        "Unique Investment Identifier",
        "Investment Name",
        "Spending $ FY2022"]]

    # Abre driver na URL
    browser.go_to(AGENCY_INVESTMENTS_URL)

    # Aguarda até carregar um elemento na página
    browser.wait_until_page_contains_element(
        "id:edit-keywords", 10
    )

    # Busca pelo nome do departamento
    browser.input_text("id:edit-keywords", agency_name)
    browser.click_button("id:edit-submit")

    # Aguarda até carregar o resultado da busca
    browser.wait_until_page_contains_element(
        "css:div.search-title-area > h2", 10
    )

    agency_spendings += collect_investment_page_data(browser)

    return agency_spendings


def collect_investment_page_data(browser):

    agency_spendings = []

    total_investment_count = browser.get_text(
        "//*[@id='search-results']/div[2]/div[1]/div[1]"
    )

    total_investment_count = int(total_investment_count.split(' of ')[1])

    pages_count = math.ceil(total_investment_count/10)

    for current_page in range(1, pages_count+1):

        investment_count = browser.get_element_count(
            "css:div.search-result-item"
        )

        if investment_count < 1:
            raise Exception("Nenhum investimento encontrado")

        for i in range(1, investment_count+1):

            investment_fieds = get_investment_data(browser, i)

            agency_spendings.append(investment_fieds)

        if current_page < pages_count:
            # Botão para paginar o resultado
            browser.click_element(
                "//*[@id='search-results']/div[2]/div[1]/div[2]/a[2]"
            )

            # Aguarda carregar os dados da página
            browser.wait_until_element_contains(
                "//*[@id='search-results']/div[2]/div[1]/div[2]/span",
                f"Page {current_page+1} of {pages_count}",
                10
            )

    return agency_spendings


def get_investment_data(browser, index):

    investment_fieds = []

    # Pega o nome do investimento e o ID
    name_id_xpath = "xpath://*[@id='search-results']/div[3]/div["
    name_id_xpath += str(index) + "]/div[1]/span[2]/a"
    name_id_string = browser.get_text(name_id_xpath)
    name_id_list = name_id_string.split('/')

    # Pega o valor do investimento
    spending_xpath = "xpath://*[@id='search-results']/div[3]/div["
    spending_xpath += str(index) + "]/div[3]/div[2]/span[2]"
    spend_value = browser.get_text(spending_xpath)
    spend_value = re.sub(r'[^0-9.,]', '', spend_value) or 0

    # Pega o link do business case
    download_xpath = "xpath: //*[@id='search-results']/div[3]/div["
    download_xpath += str(index) + "]/div[1]/div/span/a"
    if browser.is_element_visible(download_xpath):
        business_case_link = browser.get_element_attribute(
            download_xpath,
            "href"
        )

        # Inacabado
        # download_business_case(browser, business_case_link, name_id_list[1])

    # Coloca os dados do investimento na lista
    # ID
    investment_fieds.append(name_id_list[1])
    # Name
    investment_fieds.append(name_id_list[0])
    investment_fieds.append(spend_value)

    return investment_fieds


def download_business_case(browser, link, investment_id):

    # Acessa a página do business case
    browser.open_available_browser(link)

    # Aguarda carregar um elemento na página
    browser.wait_until_page_contains_element(
        "xpath://*[@id='block-data-visualizer-content']/div/fieldset[1]/legend/span",
        10
    )

    browser.print_to_pdf(OUTPUT_PATH + investment_id + ".pdf")

    # Tentei clicar e não funcionou, então mudei o caminho para o print to pdf
    # browser.click_link("//*[@id='block-data-visualizer-content']/div/a[1]")

    # browser.click_button(
    #     "//*[@id='sidebar']//print-preview-button-strip//div/cr-button[1]"
    # )

    browser.close_browser()


def main():
    try:
        logger.info("Coletor de dados iniciado")

        browser = Selenium()
        browser.open_available_browser()
        browser.set_download_directory(OUTPUT_PATH)

        sheets = []
        
        data = get_agencies_spendings(browser)
        sheets.append({"name": AGENCIES_SHEET_NAME, "data": data})
        logger.info("Sumário de despesas dos departamentos coletados")

        data = get_agency_spending(browser, TEST_AGENCY_NAME)
        sheets.append({"name": TEST_AGENCY_NAME, "data": data})
        logger.info("Despesas do departamento teste coletados")

        data_manipulation.convert_list_to_xlsx("agencies.xlsx", sheets)
    except BaseException:
        logger.exception("Falha ao extrair informações")
    finally:
        browser.close_browser()
        logger.info("Coletor de dados finalizado")


if __name__ == "__main__":
    main()
