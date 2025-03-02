import json
import os
import pprint
from io import BytesIO
from urllib import response

from PIL import Image

import requests


class VK:
    def __init__(self, vk_app_token, vk_user_id, version='5.131'):
        self.base_url = 'https://api.vk.com/method'
        self.vk_app_token = vk_app_token
        self.vk_user_id = vk_user_id
        self.version = version
        self.params = {
            'access_token': self.vk_app_token,
            'v': version,
        }
        self.images_info = []

    def check_token(self):
        url = f'{self.base_url}/users.get'
        params = {
            'fields': 'id',
        }
        params.update(self.params)
        response = requests.get(url, params=params)
        return response.json()

    def get_friends(self):
        url = f'{self.base_url}/friends.get'
        params = {
            'user_id': self.vk_user_id,
            'fields': ['city'],
            'count': 3,
        }

        params.update(self.params)
        response = requests.get(url, params=params)
        return response.json()

    def get_photos(self):
        url = f'{self.base_url}/photos.get'
        params = {
            'user_id': self.vk_user_id,
            'album_id': 'profile',
            'v': self.version,
            'extended': 'true',
            'count': 5,
        }

        try:
            response = requests.get(url, params={**self.params, **params})
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(f'Ошибка при запросе к API {e}')

        try:
            if response.status_code == 200:
                images = response.json()
        except json.decoder.JSONDecodeError as e:
            raise Exception(f'Ошибка при разборе JSON {e}')

        pprint.pp(images['response']['items'])

        for photo in images['response']['items']:
            try:
                image_date = photo['date']
                image_likes = photo['likes']['count']
                image_url = photo['sizes'][-1]['url']
                image_size = photo['sizes'][-1]['type']

                image_response = requests.get(image_url)
                image = Image.open(BytesIO(image_response.content))
                image_width, image_height = image.size

                self.images_info.append({
                    'image_date': image_date,
                    'image_likes': image_likes,
                    'image_url': image_url,
                    'image_size': image_size,
                    'image_width': image_width,
                    'image_height': image_height,
                    'image': image,
                })
            except Exception as e:
                raise Exception(f'Ошибка при обработке изображения {e}')


        pprint.pp(self.images_info)
        return self.images_info

    def download_images(self):
        images_likes_set = set()
        download_folder = "download"
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        if self.images_info:
            for image_info in self.images_info:
                likes = image_info['image_likes']
                date = image_info['image_date']

                if likes in images_likes_set:
                    filename = f'{likes}_{date}.jpg'
                else:
                    filename = f'{likes}.jpg'
                    images_likes_set.add(likes)

                full_path = os.path.join(download_folder, filename)
                image_info['image'].save(full_path)
                print(f'Изображение сохранено: {full_path}')

    def images_info_to_json(self):
        download_folder = "download"
        data = []
        if self.images_info:
            try:
                for image_info in self.images_info:
                    data.append({
                        'file_name': f'{image_info['image_likes']}.jpg',
                        'size': image_info['image_size']
                    })
                with open(f'{download_folder}/images_info.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                raise Exception(f'Не удалось получить информацию для сохранения')
