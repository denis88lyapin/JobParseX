import json
import os
from datetime import datetime
import requests


class SuperJobPlatformAPI:
    """
    Класс для работы с API SuperJob.
    """
    sj_api_secret_key = os.getenv('SJ_API_SECRET_KEY')

    def __init__(self, keywords, town) -> None:
        self.__keywords = keywords
        self.__town = town
        self.area_id = self.__get_area_id()
        self.__base_url = 'https://api.superjob.ru/2.0/vacancies/'
        self.__headers = {'X-Api-App-Id': self.sj_api_secret_key}
        self.vacancies = []

    def get_vacancies(self) -> None:
        """
        Функция возвращает все вакансии по параметрам поиска.
        """
        params = {'keyword': self.__keywords, 'town': self.area_id, 'page': 0, 'count': 100}
        vacancies_tmp = []
        while True:
            response = requests.get(self.__base_url, params=params, headers=self.__headers)
            if response.status_code == 200:
                print(f'{self.__class__.__name__} загрузкака страницы {params["page"]}')
                data = response.json()
                vacancies_tmp.extend(data['objects'])
                more_results = data['more']
                if not more_results:
                    break
                params['page'] += 1
            else:
                print('Ошибка при получении списка вакансий с API SuperJob.ru:', response.text)
                break
        filtered_vacancies = self.__filter_vacancy(vacancies_tmp)
        self.vacancies.extend(filtered_vacancies)

    @staticmethod
    def __filter_vacancy(vacancy_data: list) -> list:
        """
        Функция извлекает и конвертирует данные о вакансиях.
        :param vacancy_data:
        :return: vacancy
        """
        vacancies = []
        for vacancy in vacancy_data:
            if not vacancy["is_closed"]:
                datetime_obj = datetime.fromtimestamp(vacancy['date_published'])
                formatted_date = datetime_obj.strftime("%Y.%m.%d %H:%M:%S")
                payment_from = vacancy['payment_from'] if vacancy['payment_from'] is not None else 0
                payment_to = vacancy['payment_to'] if vacancy['payment_to'] is not None else 0
                processed_vacancy = {
                    'platform': "SuperJob",
                    "id": vacancy["id"],
                    'title': vacancy['profession'],
                    'company': vacancy['firm_name'],
                    'url': vacancy['link'],
                    'area': vacancy['town']['title'],
                    'address': vacancy['address'],
                    'candidat': vacancy['candidat'],
                    'vacancyRichText': vacancy['vacancyRichText'],
                    'date_published': formatted_date,
                    'payment': {'from': payment_from, 'to': payment_to, 'currency': vacancy["currency"]}
                }
                vacancies.append(processed_vacancy)

        return vacancies

    def __get_area_id(self):
        areas = requests.get(url="https://api.superjob.ru/2.0/regions/combined/").json()
        area_id = None
        found_town = None

        for area in areas:
            if 'title' in area and area['title'] == self.__town.title():
                found_town = area["id"]
                break

            for town in area.get('towns', []):
                if 'title' in town and town["title"] == self.__town.title():
                    found_town = town["id"]
                    break

            if found_town:
                break

        return found_town

if __name__ == "__main__":
    a = SuperJobPlatformAPI(keywords="Бухгалтер", town="Алабино")
    a.get_vacancies()
    c = a.vacancies
    print(json.dumps(c))
