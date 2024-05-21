import json
import os.path
from abc import ABC, abstractmethod

from config import DATA_PATH
import config
from vacancy import Vacancy


class AbstractWorker(ABC):

    @abstractmethod
    def read(self):
        raise NotImplementedError()

    @abstractmethod
    def write(self, value: dict):
        raise NotImplementedError()

    @abstractmethod
    def filter(self, key: str | list[str], field: str):
        raise NotImplementedError()

    @abstractmethod
    def unlink(self, value):
        raise NotImplementedError()


class JSONWorker(AbstractWorker):

    def __init__(self, file_name, model):
        self.model = model
        self.path_file = os.path.join(DATA_PATH, file_name)
        self.prepare()

    def prepare(self):
        self.__write([])

    def __write(self, value: list):
        try:
            with open(self.path_file, 'w', encoding='utf-8') as file:
                json.dump(value, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(e)

    def __read(self):
        try:
            with open(self.path_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(e)

    def read(self, limit=None) -> list[Vacancy]:
        return sorted(self.model.cast_to_object_list(self.__read()))[:limit]

    @staticmethod
    def __prepare_value(vals) -> list[Vacancy]:
        if isinstance(vals, list):
            return [obj_data.to_dict() for obj_data in vals]
        return [vals.to_dict()]

    def write(self, vals) -> bool:
        data = self.__read()
        data.extend(self.__prepare_value(vals))
        self.__write(data)
        return True

    def unlink(self, vals):
        data = self.__read()
        vals = self.__prepare_value(vals)
        data = [line for line in data if line not in vals]
        self.__write(data)
        return True

    def filter(self, filter_keys: str | list[str], field: str = None):
        data = self.__read()
        result = []
        for line in data:
            for key, value in line.items():
                if (key == field or not field) and value in filter_keys:
                    result.append(line)
        return self.model.cast_to_object_list(result)


json_db = JSONWorker('vacancies.json', model=Vacancy)
