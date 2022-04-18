# yamdb_final [![Final_yamdb](https://github.com/avemin/yamdb_final/workflows/Final_yamdb/badge.svg)](https://github.com/avemin/yamdb_final/actions/workflows/yamdb_workflow.yml)

## **Описание**
Проект Yamdb_final это готовый к запуску на любом компьютере 
проект YaMDb ко корый собирает отзывы пользователей на различные произведения.

**Технологи:**
* Python
* Django REST Framework

### Как запустить проект:

Проект доступен по адресу:
http://51.250.103.30/admin

Выполняем миграции в две команды:
```
sudo docker-compose exec web python3 manage.py migrate auth
```
```
sudo docker-compose exec web python3 manage.py migrate --fake-initial --run-syncdb
```
Создаем суперпользователя:
```
sudo docker-compose exec web python manage.py createsuperuser
```
Собираем статику:
```
sudo docker-compose exec web python manage.py collectstatic --no-input 
```
Импорт базы данных:
```
sudo docker-compose exec web python manage.py loaddata fixtures.json
```

## Шаблон наполнения env-файла:
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgresdb # имя базы данных
POSTGRES_USER=login # логин для подключения к базе данных
POSTGRES_PASSWORD=password # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY = 'asdfghjkk1234565' # ваш секретный ключик.

## Об авторе:
Автором данного проекта является студент 6 когорты курса python developer+ 
avemin, ссылка на гитхаб https://github.com/avemin/

## Примеры:
### Пример POST-запроса, получить код подтверждения на переданный email.

    [POST] .../auth/signup/

    {
        "email": "string",
        "username": "string"
    }
    
__Пример ответа:__

    {

        "email": "string",
        "username": "string"

    }


### Пример POST-запроса, получение JWT-токена в обмен на username и confirmation code.

    [POST] .../auth/token/

    {

        "username": "string",
        "confirmation_code": "string"

    }    

__Пример ответа:__

    {

        "token": "string"

    }
### Пример GET-запроса, получить список всех категорий.

    [GET] .../api/v1/categories/

__Пример ответа:__

    [

        {

            "count": 0,
            "next": "string",
            "previous": "string",
            "results": 

    [

                {
                    "name": "string",
                    "slug": "string"
                }
            ]
         }

    ]