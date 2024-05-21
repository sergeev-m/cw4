from pprint import pprint

from src.worker import JSONWorker
from src.api import hh_api, HeadHunterAPI
from src.worker import json_db
from src.vacancy import Vacancy


class UserInteraction:

    def __init__(self, api: HeadHunterAPI, worker: JSONWorker, model):
        self.model = model
        self.api = api
        self.worker = worker

    def __call__(self):
        self.get_vacancy()
        self.get_filtered_vacancies()
        self.get_ranged_vacancies()
        return self.get_top_n()

    def get_vacancy(self):
        query = input("Введите поисковый запрос: ")
        vac_qty = input('Введите количество вакансий, не больше 100: ')
        res = self.api.get_vacancies(query, vac_qty)
        obj_list = self.model.cast_to_object_list(res)
        self.worker.write(obj_list)

    def get_filtered_vacancies(self):
        filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
        if not filter_words:
            return
        return self.worker.filter(filter_words)

    def get_top_n(self):
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        return self.worker.read(top_n)

    def get_ranged_vacancies(self):
        salary_from, salary_to = map(
            lambda r: int(r.strip()),
            input("Введите диапазон зарплат(Пример: 100000 - 150000): ").split('-')
        )

        self.obj_list = [
            obj for obj in self.obj_list if obj.salary_from >= salary_from and obj.salary_to <= salary_to
        ]


vacancy_user_interaction = UserInteraction(api=hh_api, worker=json_db, model=Vacancy)


if __name__ == '__main__':
    pprint(vacancy_user_interaction())
