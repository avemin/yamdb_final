# Yamdb_final ![YaMDb Status](https://github.com/avemin/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)
## **Описание**
Проект Infra_sp2 это готовый к запуску на любом компьютере 
проект YaMDb ко корый собирает отзывы пользователей на различные произведения.

**Технологи:**
* Python
* Django REST Framework

### Как запустить проект:

Клонировать репозиторий и перейти в каталог infra:
```
git clone https://github.com/avemin/infra_sp2.git
```
```
cd infra_sp2/infra
```
Cобираем и запускаем контейнеры проекта:
```
sudo docker-compose up -d --build
```
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
SECRET_KEY = 'asdfghjkk1234565' # ваш секретный ключик 

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