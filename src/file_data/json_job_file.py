import json
import os

from src.file_data.job_file import JobFile


class JsonJobFile(JobFile):
    """
    Класс для работы с вакансиями в json файле.
    """
    def __init__(self):
        self.__file_path = os.path.join('', 'data/vacancy.json')

    import os

    def add_vacancy(self, vacancy, data_append=False):
        """
        Функция для записи (добавления) вакансий в файл json. Обработаны исключения:
        - файла нет, нет директории с файлом - создаются заново;
        - файл пустой, но функция работает в режиме добавления.
        :param vacancy:
        :param data_append:
        :return:
        """
        try:
            if not data_append:
                with open(self.__file_path, "w") as file_path:
                    data = json.dumps(vacancy, indent=2, ensure_ascii=False)
                    file_path.write(data)
            else:
                with open(self.__file_path, "r") as file_path:
                    load_data = json.load(file_path)
                with open(self.__file_path, "w") as file_path:
                    load_data.append(vacancy[0])
                    write_data = json.dumps(load_data, indent=2, ensure_ascii=False)
                    file_path.write(write_data)
        except json.JSONDecodeError:
            with open(self.__file_path, 'w') as file_path:
                data = json.dumps(vacancy, indent=2, ensure_ascii=False)
                file_path.write(data)
        except FileNotFoundError:
            os.makedirs("")
            with open(self.__file_path, "w") as file_path:
                data = json.dumps(vacancy, indent=2, ensure_ascii=False)
                file_path.write(data)

    def get_vacancies(self, search_query):
        keywords = search_query.lower().split()
        result = []

        with open(self.__file_path, 'r') as file_path:
            data = json.load(file_path)
            for vacancy in data:
                for value in vacancy.values():
                    if any(keyword in value for keyword in keywords):
                        result.append(vacancy)
        return result


    def remove_vacancy(self, vacancy_id):
        pass



if __name__ == "__main__":
    a = JsonJobFile()

    data = [{
    "platform": "HeadHunter",
    "id": "81651060",
    "title": "Заместитель главного бухгалтера",
    "company": "Ищем работу вместе",
    "url": "https://hh.ru/vacancy/81651060",
    "area": "Москва",
    "address": "",
    "candidat": "Опыт работы в производственных компаниях. Знание 1С 8.3 <highlighttext>Бухгалтерия</highlighttext>, Управление торговлей, ЗУП, MS Office. Внимательность к деталям, аккуратность...",
    "vacancyRichText": "Учет сырья, материалов. Ведение производственного учета: создание заказов на производство, списание сырья в производство, выпуск готовой продукции. Проверка производственных и...",
    "date_published": "2023.06.08 23:41:07",
    "payment": {
      "from": 80000,
      "to": 110000
    }
  },
  {
    "platform": "HeadHunter",
    "id": "79718141",
    "title": "Бухгалтер по расчету заработной платы",
    "company": "LITOKOL",
    "url": "https://hh.ru/vacancy/79718141",
    "area": "Москва",
    "address": "Москва, проезд Завода Серп и Молот, 6к1",
    "candidat": "...<highlighttext>Бухгалтерия</highlighttext> 8.3, знаете бухгалтерский учет на участках: банк, расчеты с покупателями, авансовые отчеты. Являетесь уверенным пользователем 1С <highlighttext>Бухгалтерия</highlighttext>...",
    "vacancyRichText": "Обеспечивать синхронизацию из 1С: ЗУП в 1С: <highlighttext>Бухгалтерия</highlighttext> и проводить операции по заработной плате и иным выплатам на...",
    "date_published": "2023.05.31 12:20:18",
    "payment": {
      "from": 115000,
      "to": 0
    }}]

    a.add_vacancy(data, True)
    print(str(a.get_vacancies("бухгалтер")))


