import os
import pprint
from tqdm import tqdm
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



    def upload_file(self, file_path, remote_folder, file_name):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.ya_app_token}'
        }

        remote_path = os.path.join(remote_folder, file_name).replace("\\", "/")
        upload_url = f'{self.base_url}/disk/resources/upload?path={remote_path}&overwrite=true'
        response = requests.get(upload_url, headers=headers)

        if response.status_code == 200:
            href = response.json().get('href')
            try:
                with open(file_path, 'rb') as f:
                    upload_response = requests.put(href, files={'file': f})
                    upload_response.raise_for_status()
                    print(f'Файл {file_path} успешно загружен на Я.Диск в папку {remote_folder}')

            except requests.exceptions.RequestException as e:
                raise Exception(f'Ошибка загрузки файла {e}')

    def upload_files_from_folder(self, local_folder, remote_folder):
        if not os.path.exists(local_folder):
            raise Exception(f"Локальная папка '{local_folder}' не существует.")

        for file_name in tqdm(os.listdir(local_folder), desc='Загрузка файлов на Я.Диск', unit='file'):
            local_path = os.path.join(local_folder, file_name)
            if os.path.isfile(local_path):
                # remote_path = os.path.join(remote_folder, file)
                self.upload_file(local_path, remote_folder, file_name)