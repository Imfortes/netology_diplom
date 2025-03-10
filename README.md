# Курсовая работа «Резервное копирование»

## Задание:
Нужно написать программу, которая будет:
- Получать фотографии с профиля. Для этого нужно использовать метод photos.get.
- Сохранять фотографии максимального размера(ширина/высота в пикселях) на Я.Диске.
- Для имени фотографий использовать количество лайков. Если количество лайков одинаково, то добавить дату загрузки.
- Сохранять информацию по фотографиям в json-файл с результатами.

## Входные данные:
Пользователь вводит:
- id пользователя vk;
- токен с Полигона Яндекс.Диска. Важно: Токен публиковать в github не нужно!

## Выходные данные:
- json-файл с информацией по файлу:

```
    [{
        "file_name": "34.jpg",
        "size": "z"
    }]
```

- Измененный Я.диск, куда добавились фотографии.

## Обязательные требования к программе:
- Использовать REST API Я.Диска и ключ, полученный с полигона.
- Для загруженных фотографий нужно создать свою папку.
- Сохранять указанное количество фотографий(по умолчанию 5) наибольшего размера (ширина/высота в пикселях) на Я.Диске
- Сделать прогресс-бар или логирование для отслеживания процесса программы.
- Код программы должен удовлетворять PEP8.
- У программы должен быть свой отдельный репозиторий.
- Все зависимости должны быть указаны в файле requiremеnts.txt.

## Необязательные требования к программе:
- Сохранять фотографии и из других альбомов.
- Сохранять фотографии на Google.Drive.