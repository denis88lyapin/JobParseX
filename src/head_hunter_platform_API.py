import json
from datetime import datetime

from src.job_platform_API import JobPlatformAPI
import requests

class HeadHunterPlatformAPI(JobPlatformAPI):
    base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, key_word=''):
        all_vacancies = []
        page = 0
        per_page = 100  # Количество вакансий на каждой странице
        total_pages = 1

        while page < total_pages:
            params = {
                'text': key_word,
                'page': page,
                'per_page': per_page
            }
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                vacancies = response.json()

                all_vacancies.extend(vacancies["items"])
                total_pages = vacancies['pages']
                page += 1
            else:
                print('Ошибка при получении списка вакансий с HeadHunter.ru:', response.text)
                return []
        processed_vacancies = []
        for vacancy in all_vacancies:
            if vacancy['type']['id'] == 'open':
                address = vacancy['address']
                address_raw = address['raw'] if address else ""
                salary = vacancy['salary']
                salary_from = salary['from'] if salary else None
                salary_to = salary['to'] if salary else None
                datetime_obj = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
                formatted_date = datetime_obj.strftime("%Y.%m.%d %H:%M:%S")
                processed_vacancy = {
                    'platform': "HeadHunter",
                    'title': vacancy['name'],
                    'company': vacancy['employer']['name'],
                    'url': vacancy['alternate_url'],
                    'area': vacancy['area']['name'],
                    'address': address_raw,
                    'candidat': vacancy['snippet']['requirement'],
                    'vacancyRichText': vacancy['snippet']['responsibility'],
                    'date_published': formatted_date,
                    'payment': [salary_from, salary_to]
                }
                processed_vacancies.append(processed_vacancy)

        return processed_vacancies


if __name__ == "__main__":
    a = HeadHunterPlatformAPI()
    vacancies = a.get_vacancies(key_word='бухгалтер')
    print(len(vacancies))
    print(json.dumps(vacancies, indent=2, ensure_ascii=False))
