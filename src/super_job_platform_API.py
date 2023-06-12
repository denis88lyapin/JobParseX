import json
import os
from datetime import datetime

from src.job_platform_API import JobPlatformAPI
import requests

class SuperJobPlatformAPI(JobPlatformAPI):
    """
    Класс для работы с API SuperJob.
    """
    sj_api_secret_key = os.getenv('SJ_API_SECRET_KEY')
    base_url = 'https://api.superjob.ru/2.0/vacancies/'

    def get_vacancies(self, key_word=''):
        headers = {
            'X-Api-App-Id': self.sj_api_secret_key
        }
        params = {
            'keyword': key_word
        }

        response = requests.get(self.base_url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            vacancies = data['objects']

            processed_vacancies = []
            for vacancy in vacancies:
                if not vacancy["is_closed"]:
                    datetime_obj = datetime.fromtimestamp(vacancy['date_published'])
                    formatted_date = datetime_obj.strftime("%Y.%m.%d %H:%M:%S")
                    processed_vacancy = {
                        'platform': "SuperJob",
                        'title': vacancy['profession'],
                        'company': vacancy['firm_name'],
                        'url': vacancy['link'],
                        'area': vacancy['town']['title'],
                        'address': vacancy['address'],
                        'candidat': vacancy['candidat'],
                        'vacancyRichText': vacancy['vacancyRichText'],
                        'date_published': formatted_date,
                        'payment': [vacancy['payment_from'], vacancy['payment_to']]
                        }
                    processed_vacancies.append(processed_vacancy)

            return processed_vacancies
        else:
            print('Ошибка при получении списка вакансий с API SuperJob.ru:', response.text)
            return []




if __name__ == "__main__":

    a = SuperJobPlatformAPI()
    print(len(json.dumps(a.get_vacancies(key_word='python'), indent=2, ensure_ascii=False)))
    print(json.dumps(a.get_vacancies(key_word='python'), indent=2, ensure_ascii=False))
