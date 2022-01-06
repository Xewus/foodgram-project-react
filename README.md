# Foodgram

[![License](https://img.shields.io/badge/License-BSD_2--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)

![workflow](https://github.com/Xewus/Foodgram/actions/workflows/main.yml/badge.svg)

-Diploma work for Yandex-\
-Frontend provided by the customer-\

http://my-ya.ml

Информация для ревью (впоследствии будет удалена):

```
Для docker-compose необходим */backend/.env, если пустой, то будет использована прилагаемая БД со следующими данными:
```
```
superuser: q@q.qq
```
```
password: q
```
```
Пароль остальных пользователей: aqswdefr
```

Here you can share recipes of dishes, add them to favorites and display a shopping list for cooking your favorite dishes.
To preserve order - only administrators are allowed to create tags and ingredients.


Tecnhologies:
- Python 3.10
- Django 4.0
- Django REST
- Nginx
- Docker

To deploy this project need next actions:

- Install Docker on your server
```
sudo apt install docker.io
```
- Install Docker Compose (for Linux)
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
- Get permissions for docker-compose
```
sudo chmod +x /usr/local/bin/docker-compose
```
- Download project with SSH (in general, you only need a folder 'infra/')
```
git@github.com:Xewus/foodgram-project-react.git
```

- Create project directory on your server
```
mkdir foodgram && cd foodgram/
```
- Copy files from 'infra/'  there:
```
scp infra/* <server user>@<server address>:/home/<server user>/foodgram/
```
- Create env-file:
```
touch foodgram/.env
```
- Fill in the env-file like it:
```
DEBUG=False
SECRET_KEY=<Your_any_long_string>
ALLOWED_HOSTS='localhost, 127.0.0.1, <Your_host>'
CSRF_TRUSTED_ORIGINS='http://localhost, http://127.0.0.1, http://<Your_host>'
DB_ENGINE='django.db.backends.postgresql'
DB_NAME='postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD=<Your_password>
DB_HOST='db'
DB_PORT=5432
```
- Run docker-compose
```
sudo docker-compose up -d
```
Wait a few seconds...
Your service is work!
![Иллюстрация к проекту](https://github.com/Xewus/Foodgram/raw/master/image_path/image.png)

# Enjoy your meal !