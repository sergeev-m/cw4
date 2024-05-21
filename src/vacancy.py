class Vacancy:
    def __init__(self, name: str, salary_from, salary_to, alternate_url:str, city:str, employment:str, requirement:str, responsibility:str):
        self.name = name
        self.alternate_url = alternate_url
        self.city = city
        self.salary_from = salary_from if salary_from else 0
        self.salary_to = salary_to if salary_to else 0
        self.employment = employment
        self.requirement = requirement
        self.responsibility = responsibility

    def __lt__(self, other):
        salary_to = self.salary_to if self.salary_to else float('inf')
        other_salary_to = other.salary_to if other.salary_to else float('inf')
        if salary_to < other_salary_to:
            return True
        return self.salary_from < other.salary_from

    def __eq__(self, other):
        return self.salary_to == other.salary_to and self.salary_from == other.salary_from

    def __gt__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    @staticmethod
    def cast_to_object_list(vacancy_list):
        result = []
        for vacancy in vacancy_list:
            obj = Vacancy(
                name=vacancy['name'],
                salary_from=vacancy['salary']['from'] if vacancy['salary'] else None,
                salary_to=vacancy['salary']['to'] if vacancy['salary'] else None,
                alternate_url=vacancy['alternate_url'],
                city=vacancy['area']['name'],
                employment=vacancy['employment']['name'],
                requirement=vacancy['snippet']['requirement'],
                responsibility=vacancy['snippet']['responsibility']
            )
            result.append(obj)
        return result

    def to_dict(self):
        return {
            'name': self.name,
            'salary_from': self.salary_from,
            'salary_to': self.salary_to,
            'alternate_url': self.alternate_url,
            'city': self.city,
            'employment': self.employment,
            'requirement': self.requirement,
            'responsibility': self.responsibility
        }
