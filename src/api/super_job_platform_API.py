import os
from datetime import datetime

from src.api.job_platform_API import JobPlatformAPI
import requests


class SuperJobPlatformAPI(JobPlatformAPI):
    """
    Класс для работы с API SuperJob. Максимальное количество
    вакансий - 500 (ограничение API)
    """
    sj_api_secret_key = os.getenv('SJ_API_SECRET_KEY')

    def __init__(self):
        self.base_url = 'https://api.superjob.ru/2.0/vacancies/'

    def get_vacancies(self, key_word=''):
        """
        Функция возвращает все вакансии по параметрам поиска.
        :param key_word:
        :return: vacancies
        """
        headers = {'X-Api-App-Id': self.sj_api_secret_key}
        params = {'keyword': key_word, 'page': 0, 'count': 100}
        vacancies = []

        while True:
            response = requests.get(self.base_url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                current_vacancies = data['objects']
                vacancies.extend(current_vacancies)


                more_results = data['more']
                if not more_results:
                    break

                params['page'] += 1
            else:
                print('Ошибка при получении списка вакансий с API SuperJob.ru:', response.text)
                return None

        filtered_vacancies = self.__filter_vacancy(vacancies)
        return filtered_vacancies



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


# if __name__ == "__main__":
#     a = SuperJobPlatformAPI()
#     # b = a.get_vacancies(key_word='python')
#     # print(len(b))
#     # print(json.dumps(b, indent=2, ensure_ascii=False))
#     print(json.dumps(a.get_vacancies(key_word='python 100000 Москва'), indent=2, ensure_ascii=False))
