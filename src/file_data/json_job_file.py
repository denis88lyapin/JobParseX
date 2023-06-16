import json
import os

from src.file_data.job_file import JobFile


class JsonJobFile(JobFile):
    """
    Класс для работы с вакансиями в json файле.
    """
    def __init__(self):
        self.__file_path = os.path.join('data', 'vacancy.json')

    import os

    def add_vacancy(self, vacancy, data_append=False) -> None:
        """
        Функция для записи (добавления) вакансий в файл json. Обработаны исключения:
        - файла нет, нет директории с файлом - создаются заново;
        - файл пустой, но функция работает в режиме добавления.
        """
        try:
            if not data_append:
                self.__write_file(vacancy)
            else:
                load_data = self.__read_file()
                for item in vacancy:
                    load_data.append(item)
                self.__write_file(load_data)
        except json.JSONDecodeError:
            self.__write_file(vacancy)
        except FileNotFoundError:
            os.makedirs("data")
            self.__write_file(vacancy)

    def get_vacancies(self, search_query='') -> list:
        """
        Функция для поиска вакансий по ключевым словам.
        """
        keywords = search_query.lower().split()
        result = []
        data = self.__read_file()
        self.__search_in_data(data, keywords, result)
        return result

    def remove_vacancy(self, vacancy_id):
        data = []
        data_tmp = self.__read_file()
        for item in data_tmp:
            if vacancy_id != item["id"]:
                data.append(item)
            self.__write_file(data_tmp)

    def __read_file(self):
        """
        Функция чтения данных из файла.
        """
        with open(self.__file_path, "r") as file:
            data = json.load(file)
        return data

    def __write_file(self, data):
        """
        Функция записи данных в файл.
        """
        with open(self.__file_path, "w") as file:
            write_data = json.dumps(data, indent=2, ensure_ascii=False)
            file.write(write_data)


    def __search_in_data(self, data, keywords, result):
        """
        Рекурсивная функция, для поиска во вложенных данных.
        """
        for item in data:
            if isinstance(item, dict):
                for key, value in item.items():
                    if isinstance(value, (str, float, int)):
                        if any(keyword in str(value).lower() for keyword in keywords):
                            result.append(item)
                            break
                    elif isinstance(value, (dict, list)):
                        self.__search_in_data([value], keywords, result)
            elif isinstance(item, list):
                self.__search_in_data(item, keywords, result)



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

    a = JsonJobFile()
    a.add_vacancy(data, data_append=True)

    a.remove_vacancy("81651060")


