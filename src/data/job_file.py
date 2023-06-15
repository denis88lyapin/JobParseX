from abc import ABC, abstractmethod


class JobFile(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancy(self, search_query):
        pass

    @abstractmethod
    def remove_vacancy(self, vacancy_id):
        pass
