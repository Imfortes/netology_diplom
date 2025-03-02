import configparser
from pprint import pprint

import vk_module
import ya_module

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('.env')

    vk_app_token = config['VK']['VK_APP_TOKEN']
    vk_user_id = config['VK']['VK_USER_ID']

    ya_app_token = config['YA']['YA_APP_TOKEN']

    vk = vk_module.VK(vk_app_token, vk_user_id)
    ya = ya_module.YA(ya_app_token)
    # pprint(vk.check_token())
    # pprint(vk.get_friends())
    # pprint(vk.get_photos())

    # vk.get_photos()
    # vk.download_images()
    # vk.images_info_to_json()

    # ya.check_token()
    ya.create_folder('test')
