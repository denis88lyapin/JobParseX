from datetime import datetime
class Vacancy:

    __slots__ = ('id', "platform", "title", "company", "url", "area", "address", "candidat",
                 "vacancy_rich_text", "date_published", "payment", "priority")
    """
    Класс для работы с вакансиями. Инициализируется по данным потомков класса JobPlatformAPI.
    Хранит список вакансий. Поддерживает методы сравнения и сортировки вакансий по зарплате и дате.
    """
    all = []
    def __init__(self, vacancy: dict) -> None:
        try:
            if vacancy:
                self.platform = vacancy.get('platform', 'нет данных')
                self.id = vacancy.get("id")
                self.title = vacancy.get('title', 'нет данных')
                self.company = vacancy.get('company', 'нет данных')
                self.url = vacancy.get('url', 'нет данных')
                self.area = vacancy.get('area', 'нет данных')
                self.address = vacancy.get('address', 'нет данных')
                self.candidat = vacancy.get('candidat', 'нет данных')
                self.vacancy_rich_text = vacancy.get('vacancyRichText', 'нет данных')
                self.payment = vacancy.get('payment', 'нет данных')
                date_str = vacancy.get('date_published')
                self.date_published = datetime.strptime(date_str, '%Y.%m.%d %H:%M:%S')
                self.priority = False
                Vacancy.all.append(self)

            else:
                raise ValueError("Вакансия не найдена")
        except ValueError as error:
            print(str(error))
            print("Повторите запрос")

    def __str__(self):
        return f'id: {self.id}\n' \
               f'Title: {self.title}\n' \
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
            payment_1 = self.get_payment()
            payment_2 = other.get_payment()

            return payment_1 < payment_2

    def get_payment(self):
        """
        Функция возвращает зарплату.
        При условии, что зарплата "от" и "до" больше 0, присваивается среднее значение.
        При условии, что "от" равно 0 или "до" равно 0, то присваивается значение не равное 0.
        При условии, что "от" и "до" равны 0, то присваивается 0.
        :return:
        """
        payment_from = int(self.payment.get("from", 0))
        payment_to = int(self.payment.get('to', 0))
        if payment_to > 0 and payment_from > 0:
            payment = (payment_to + payment_from) / 2
        elif payment_from == 0:
            payment = payment_to
        else:
            payment = payment_from
        return payment

    def sort_vacancy_payment(self) -> None:
        """
        Функция сортирует вакансии по зарплате.
        """
        Vacancy.all.sort(key=lambda vacancy: vacancy.get_payment())

    def sort_vacancy_date(self):
        """
        Функция сортирует вакансии по зарплате.
        """
        Vacancy.all.sort(key=lambda vacancy: vacancy.date_published, reverse=True)

    def delete_vacancy(self, vacancy_id):
        """
        Функция удаляет вакансию из списка Vacancy.all на основе указанного идентификатора (id).
        """
        try:
            if vacancy_id.isdigit():
                vacancy_found = False
                filtered_vacancies = filter(lambda vacancy: vacancy.id == vacancy_id, Vacancy.all)
                for vacancy in filtered_vacancies:
                    Vacancy.all.remove(vacancy)
                    vacancy_found = True

                if not vacancy_found:
                    raise ValueError("Вакансия не найдена. Введите корректный идентификатор вакансии.")
            else:
                raise ValueError("Идентификатор вакансии должен состоять только из цифр.")
        except ValueError as error:
            print(str(error))


# if __name__ == '__main__':
#     data = [{
#     "platform": "HeadHunter",
#     "id": "81651060",
#     "title": "Заместитель главного бухгалтера",
#     "company": "Ищем работу вместе",
#     "url": "https://hh.ru/vacancy/81651060",
#     "area": "Москва",
#     "address": "",
#     "candidat": "Опыт работы в производственных компаниях. Знание 1С 8.3 <highlighttext>Бухгалтерия</highlighttext>, Управление торговлей, ЗУП, MS Office. Внимательность к деталям, аккуратность...",
#     "vacancyRichText": "Учет сырья, материалов. Ведение производственного учета: создание заказов на производство, списание сырья в производство, выпуск готовой продукции. Проверка производственных и...",
#     "date_published": "2023.06.08 23:41:07",
#     "payment": {
#       "from": 80000,
#       "to": 110000
#     }
#   },
#   {
#     "platform": "HeadHunter",
#     "id": "79718141",
#     "title": "Бухгалтер по расчету заработной платы",
#     "company": "LITOKOL",
#     "url": "https://hh.ru/vacancy/79718141",
#     "area": "Москва",
#     "address": "Москва, проезд Завода Серп и Молот, 6к1",
#     "candidat": "...<highlighttext>Бухгалтерия</highlighttext> 8.3, знаете бухгалтерский учет на участках: банк, расчеты с покупателями, авансовые отчеты. Являетесь уверенным пользователем 1С <highlighttext>Бухгалтерия</highlighttext>...",
#     "vacancyRichText": "Обеспечивать синхронизацию из 1С: ЗУП в 1С: <highlighttext>Бухгалтерия</highlighttext> и проводить операции по заработной плате и иным выплатам на...",
#     "date_published": "2023.05.31 12:20:18",
#     "payment": {
#       "from": 115000,
#       "to": 0
#     }}]
#
#
#
#     for b in data:
#         c = Vacancy(b)
#
#     print(c.all)
#
#     c.delete_vacancy("79718141")
#     print(c.all)






