
class Vacancy:

    __slots__ = ("platform", "title", "company", "url", "area", "address", "candidat",
                 "vacancy_rich_text", "date_published", "payment")
    """
    Класс для работы с вакансиями. Инициализируется по данным потомков класса JobPlatformAPI.
    Хранит список вакансий. Поддерживает методы сравнения и сортировки вакансий по зарплате и дате.
    """
    all = []
    def __init__(self, vacancy: dict) -> None:
        try:
            if vacancy:
                self.platform = vacancy.get('platform', 'нет данных')
                self.title = vacancy.get('title', 'нет данных')
                self.company = vacancy.get('company', 'нет данных')
                self.url = vacancy.get('url', 'нет данных')
                self.area = vacancy.get('area', 'нет данных')
                self.address = vacancy.get('address', 'нет данных')
                self.candidat = vacancy.get('candidat', 'нет данных')
                self.vacancy_rich_text = vacancy.get('vacancyRichText', 'нет данных')
                self.date_published = vacancy.get('date_published', 'нет данных')
                self.payment = vacancy.get('payment', 'нет данных')
                Vacancy.all.append(self)
            else:
                raise ValueError("Вакансия не найдена")
        except ValueError as error:
            print(str(error))
            print("Повторите запрос")

    def __str__(self):
        return f'"Title: {self.title}\n' \
               f'Payment: {self.payment}\n' \
               f'Area: {self.area}\n' \
               f'URL: {self.url}'

    def __lt__(self, other):
        if isinstance(other, Vacancy):
            """
            Функция сравнения зарплат 2-х вакансий класса Vacancy.
            При условии, что зарплата "от" и "до" больше 0, сравнивается среднее значение.
            При условии, что "от" равно 0 или "до" равно 0, то сравнивается значение не равное 0.
            При условии, что "от" и "до" равны 0, то сравнивается 0.
            """
            payment_from_1 = int(self.payment.get("from", 0))
            payment_to_1 = int(self.payment.get('to', 0))
            payment_from_2 = int(other.payment.get("from", 0))
            payment_to_2 = int(other.payment.get('to', 0))

            if payment_to_1 > 0 and payment_from_1 > 0:
                payment_1 = (payment_to_1 + payment_from_1) / 2
            elif payment_from_1 == 0:
                payment_1 = payment_to_1
            else:
                payment_1 = payment_from_1

            if payment_to_2 > 0 and payment_from_2 > 0:
                payment_2 = (payment_to_2 + payment_from_2) / 2
            elif payment_from_2 == 0:
                payment_2 = payment_to_2
            else:
                payment_2 = payment_from_2

            return payment_1 < payment_2






if __name__ == '__main__':
    data = {
    "platform": "SuperJob",
    "title": "Специалист по парсерам",
    "company": "JOBCART.RU",
    "url": "https://www.superjob.ru/vakansii/specialist-po-parseram-46449440.html",
    "area": "Москва",
    "address": "г Москва, ул Каланчевская, д 20",
    "candidat": "Вакансия компании \"MARPLA\"\nМARketPLAce - Сервис анализа поисковых запросов на Wildberries.\nОбязанности:\n- Разработка и сопровождение парсера для сбора данных с маркетплейса Wildberries.\nТребования:\n- Положительный опыт работы в команде;\n- Выходить во внерабочее время (при необходимости), для устранения критических и аварийных багов парсера;\n- Высшее техническое образование;\n- Опыт высоконагруженного парсинга:\nмногопоточный парсинг через прокси в несколько тысяч потоков;\nот 100 млн запросов в сутки;\nот 0.5 млрд записей результатов в сутки;\n- Знание python, pandas;\n- Понимание принципов работы поисковых систем, обязательных требований к сайтам;\n- ООП, структуры данных, базовые алгоритмы и понимание их сложности, базовое знание HTML/CSS/JS, базовый Git.\nУсловия:\n- Удаленный формат работы;\n- Разнообразные интересные мотивирующие задачи;\n- Своевременная выплата заработной платы.",
    "vacancyRichText": "<p>Вакансия компании \"MARPLA\"</p><p>МARketPLAce - Сервис анализа поисковых запросов на Wildberries.</p>Обязанности:<p>- Разработка и сопровождение парсера для сбора данных с маркетплейса Wildberries.</p>Требования:<p>- Положительный опыт работы в команде;<br />- Выходить во внерабочее время (при необходимости), для устранения критических и аварийных багов парсера;<br />- Высшее техническое образование;<br />- Опыт высоконагруженного парсинга:<br />многопоточный парсинг через прокси в несколько тысяч потоков;<br />от 100 млн запросов в сутки;<br />от 0.5 млрд записей результатов в сутки;<br />- Знание python, pandas;<br />- Понимание принципов работы поисковых систем, обязательных требований к сайтам;<br />- ООП, структуры данных, базовые алгоритмы и понимание их сложности, базовое знание HTML/CSS/JS, базовый Git.</p>Условия:<p>- Удаленный формат работы;<br />- Разнообразные интересные мотивирующие задачи;<br />- Своевременная выплата заработной платы.</p>",
    "date_published": "2023.06.08 16:05:18",
    "payment": {
      "from": 100000,
      "to": 0
    }}
    data2={
    "platform": "HeadHunter",
    "title": "Главный бухгалтер",
    "company": "Безопасность",
    "url": "https://hh.ru/vacancy/81551289",
    "area": "Москва",
    "address": "Москва, Щёлковское шоссе, 97",
    "candidat": "Владение программами на уровне уверенного пользователя: MS Office (Word, Excel), 1С: <highlighttext>Бухгалтерия</highlighttext> 8.3, УНФ 8.3 , ЗУП, СБИС...",
    "vacancyRichText": "Ведение бухгалтерского и налогового учета в полном объеме (книги покупок/продаж, учет материалов, затрат, основных средств (в т.ч. ",
    "date_published": "2023.06.11 15:09:18",
    "payment": {
      "from": 0,
      "to": 120000
    }}

    a = Vacancy(data)

    b = Vacancy(data2)
    print(a.__lt__(b))
    print(Vacancy.all)
