from api.head_hunter_platform_API import HeadHunterPlatformAPI
from api.super_job_platform_API import SuperJobPlatformAPI
from file_data.json_job_file import JsonJobFile
from vacancy.vacancy import Vacancy
class JobParseX:
    def __call__(self, *args, **kwargs):
        while True:
            self.title_page()
            try:
                command = int(input().strip())
                if command == 1:
                    Page1()()
                elif command == 2:
                    pass
                elif command == 0:
                    exit()
                else:
                    raise ValueError
            except ValueError:
                print("Недопустимая команда")

    def title_page(self):
        print("JobParseX - программа для поиска и подбора вакансий\n", "_" * 50)
        print("Введите команду:\n"
              "1. - обновить базу данных с платформами\n"
              "2. - загрузить вакансии из базы данных\n"
              "0. - выход из приложения")


class Page1:
    def __init__(self):
        self.apis = [SuperJobPlatformAPI, HeadHunterPlatformAPI]
        self.data = []

    def __call__(self, *args, **kwargs):
        while True:
            print("Вы выбрали запрос вакансий к платформам SuperJob и HeadHunter\n", "_" * 60)
            print("Введите команду:\n"
                  "1. - запрос к платформе SuperJob\n"
                  "2. - запрос к платформе HeadHunter\n"
                  "3. - запрос ко всем платформам\n"
                  "0. - назад")
            try:
                command = int(input().strip())
                if command == 1:
                    keywords = input("Введите поисковый запрос: ")
                    self.search_vacancies(self.apis[0](keywords=keywords))
                elif command == 2:
                    keywords = input("Введите поисковый запрос: ")
                    self.search_vacancies(self.apis[1](keywords=keywords))
                elif command == 3:
                    keywords = input("Введите поисковый запрос: ")
                    for api in self.apis:
                        self.search_vacancies(api(keywords=keywords))
                elif command == 0:
                    print("Завершение работы программы")
                    exit()
                else:
                    raise ValueError
            except ValueError:
                print("Недопустимая команда")

    def search_vacancies(self, api):
        api.get_vacancies()
        vacancies = api.vacancies
        self.data.clear()

        self.data.extend(vacancies)

        path = JsonJobFile()

        if len(self.data) > 0:
            print("Вакансии успешно загружены\n"
                  "1. - перезаписать базу данных\n"
                  "2. - добавить в базу данных\n"
                  "0. - выйти")
            user_choice = int(input())

            if user_choice == 1:
                path.add_vacancy(self.data, data_append=False)
            elif user_choice == 2:
                path.add_vacancy(self.data, data_append=True)
            elif user_choice == 0:
                return
        else:
            print("Вакансия не найдена. Повторите запрос")



if __name__ == "__main__":
    JobParseX()()


