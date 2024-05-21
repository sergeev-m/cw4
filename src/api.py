import requests

from abc import ABC, abstractmethod
from requests import HTTPError

import config


class AbstractApi(ABC):

    @abstractmethod
    def get_vacancies(self, *args, **kwargs):
        pass


class HeadHunterAPI(AbstractApi):
    def __init__(self, url: str):
        self.url = url
        self.params = {
            'text': '',
            'page': 0,
            'per_page': 100
        }

    def get_vacancies(self, keyword, vac_qty):
        self.params.update({'text': keyword})
        try:
            res = requests.get(self.url, params=self.params)
            res.raise_for_status()
            return res.json()['items']
        except HTTPError as e:
            print(e)


hh_api = HeadHunterAPI(config.hh_url)
