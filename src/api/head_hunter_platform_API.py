from datetime import datetime
from src.api.job_platform_API import JobPlatformAPI
import requests


class HeadHunterPlatformAPI(JobPlatformAPI):
    """
    Класс для работы с API SuperJob.
    """
    def __init__(self, keywords) -> None:
        self.keywords = keywords
        self.base_url = "https://api.hh.ru/vacancies"
        self.vacancies = []

    def get_vacancies(self) -> None:
        """
        Функция возвращает вакансии по параметрам поиска.
        """
        vacancies_tmp = []
        page = 0
        total_pages = 1

        while page < total_pages:
            params = {'text': self.keywords, 'page': page, 'per_page': 100}
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                print(f'{self.__class__.__name__} загрузкака страницы {page}')
                data = response.json()
                vacancies_tmp.extend(data["items"])
                total_pages = data['pages']
                page += 1
            else:
                print('Ошибка при получении списка вакансий с HeadHunter.ru:', response.text)
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
            if vacancy['type']['id'] == 'open':
                address = vacancy['address']
                address_raw = address['raw'] if address else None
                salary = vacancy['salary']
                salary_from = salary['from'] if salary else 0
                salary_to = salary['to'] if salary else 0
                datetime_obj = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
                formatted_date = datetime_obj.strftime("%Y.%m.%d %H:%M:%S")
                processed_vacancy = {
                    'platform': "HeadHunter",
                    'id': vacancy["id"],
                    'title': vacancy['name'],
                    'company': vacancy['employer']['name'],
                    'url': vacancy['alternate_url'],
                    'area': vacancy['area']['name'],
                    'address': address_raw,
                    'candidat': vacancy['snippet']['requirement'],
                    'vacancyRichText': vacancy['snippet']['responsibility'],
                    'date_published': formatted_date,
                    'payment': {'from': salary_from, 'to': salary_to}
                }
                vacancies.append(processed_vacancy)
        return vacancies


if __name__ == "__main__":
    a = HeadHunterPlatformAPI('бухгалтер 100000 Москва')
    a.get_vacancies()
    print(a.vacancies)
