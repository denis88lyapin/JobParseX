import os
from datetime import datetime
import requests

class SuperJobPlatformAPI:
    """
    Класс для работы с API SuperJob. Максимальное количество
    вакансий - 500 (ограничение API)
    """
    sj_api_secret_key = os.getenv('SJ_API_SECRET_KEY')

    def __init__(self, key_words):
        self.key_words = key_words
        self.base_url = 'https://api.superjob.ru/2.0/vacancies/'
        self.headers = {'X-Api-App-Id': self.sj_api_secret_key}
        self.vacancies = []

    def get_vacancies(self):
        """
        Функция возвращает все вакансии по параметрам поиска.
        """
        params = {'keyword': self.key_words, 'page': 0, 'count': 100}
        vacancies_tmp = []
        while True:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                vacancies_tmp.extend(data['objects'])
                more_results = data['more']
                if not more_results:
                    break
                params['page'] += 1
            else:
                print('Ошибка при получении списка вакансий с API SuperJob.ru:', response.text)
        filtered_vacancies = self._filter_vacancy(vacancies_tmp)
        self.vacancies.extend(filtered_vacancies)

    @staticmethod
    def _filter_vacancy(vacancy_data):
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
                    'payment': {'from': vacancy['payment_from'], 'to': vacancy['payment_to']}
                }
                vacancies.append(processed_vacancy)

        return vacancies


if __name__ == "__main__":
    a = SuperJobPlatformAPI("бухгалтер Москва")
    a.get_vacancies()
    print(a.vacancies)

