import requests
from bs4 import BeautifulSoup

HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "accept": "*/*"
}


def get_smartphones_list_html(url, headers):
    response = requests.get(url=url, headers=headers)
    return response.text


def get_smartphones_info_telefon_kg(smartphones_html_string) -> list:
    soup = BeautifulSoup(smartphones_html_string, "html.parser")
    smartphones_objects = soup.find_all("div", class_="product-thumb thumbnail")
    smartphones_data_list = []
    for each_smartphone in smartphones_objects:
        smartphones_data_list.append(each_smartphone.find('h4').get_text() +
                                     "\n" +
                                     each_smartphone.find('p', class_='price').get_text()
                                     .replace('\n                                    ', '')
                                     .replace('.                                                    ', '') +
                                     "\n" + each_smartphone.find('a')['href']
                                     )
    return smartphones_data_list





# def parse_to_string_model_and_price(smartphones_data_dict: dict, each_smartphone_key) -> str:
#     return smartphones_data_dict[each_smartphone_key]


