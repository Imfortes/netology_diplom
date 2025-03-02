import pprint
from wsgiref import headers

import requests

class YA:
    def __init__(self, ya_app_token):
        self.base_url = 'https://cloud-api.yandex.net/v1'
        self.ya_app_token = ya_app_token

    def check_token(self):
        url = f'{self.base_url}/disk/resources/files'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.ya_app_token}'
        }

        response = requests.get(url, headers=headers)

        pprint.pp(response.json())

    def create_folder(self, path):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.ya_app_token}'
        }

        try:
            requests.put(f'{self.base_url}/disk/resources?path={path}', headers=headers)
        except requests.exceptions.RequestException as e:
            raise Exception(f'Папка не была создана, {e}')

    def post_files(self):
        url = f'{self.base_url}/disk/resources/files'