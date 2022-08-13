# Foodgram

![workflow](https://github.com/Xewus/Foodgram/actions/workflows/main.yml/badge.svg)

#### *Diploma work for Yandex*

***
Господа, раз уж скачиваете (собственно, для этого оно и открыто) справа вверху можно тыкнуть звёздочку.  
П.С. В `docker-compose.yml` в настройках для `nginx` вам нужно будет сменить порт `8001` на `80`.
У меня так настроено, потому что на одном сервере и IP висит несколько сайтов.
***

## Tecnhologies:
- Python 3.10
- Django 4.0
- Django REST framework 3.13
- Nginx
- Docker
- Postgres


## http://foodgram.gq


Here you can share recipes of dishes, add them to favorites and display a shopping list for cooking your favorite dishes.
To preserve order - only administrators are allowed to create tags and ingredients.

### To deploy this project need the next actions:
- Download project with SSH (actually you only need the folder 'infra/')
```
git@github.com:Xewus/foodgram-project-react.git
```
- Connect to your server:
```
ssh <server user>@<server IP>
```
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
- Create project directory (preferably in your home directory)
```
mkdir foodgram && cd foodgram/
```
- Create env-file:
```
touch .env
```
- Fill in the env-file like it:
```
DEBUG=False
SECRET_KEY=<Your_some_long_string>
ALLOWED_HOSTS='localhost, 127.0.0.1, <Your_host>'
CSRF_TRUSTED_ORIGINS='http://localhost, http://127.0.0.1, http://<Your_host>'
DB_ENGINE='django.db.backends.postgresql'
DB_NAME='postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD=<Your_password>
DB_HOST='db'
DB_PORT=5432
```
- Copy files from 'infra/' (on your local machine) to your server:
```
scp -r infra/* <server user>@<server IP>:/home/<server user>/foodgram/
```
- Run docker-compose
```
sudo docker-compose up -d
```
Wait a few seconds...
Your service is work!
![Иллюстрация к проекту](https://github.com/Xewus/Foodgram/blob/master/screen.png)

## Enjoy your meal !

If you need, you can use the list of ingredients offered by us to write
recipes.
Upload it to the database with the following command 
### (this will also add a superuser with username - "qqq", password - "q", email - "q@q.qq
## DON'T FORGET TO CHANGE PASSWORD !!!):
```
sudo docker exec -it foodgram_backend_1 python manage.py loaddata data/dump.json
```

### *Backend by:*
https://github.com/Xewus
### *Frontend by:*
https://github.com/yandex-praktikum/foodgram-project-react
