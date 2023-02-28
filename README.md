# Foodgram

![workflow](https://github.com/Xewus/Foodgram/actions/workflows/main.yml/badge.svg)

***
Господа, раз уж скачиваете (собственно, для этого оно и открыто) справа вверху можно тыкнуть :star: .  
:warning: В `docker-compose.yml` в настройках для `nginx` вам нужно будет сменить порт :eight::zero::zero::one: на :eight::zero:.

У меня так настроено, потому что на одном сервере и IP висит несколько сайтов.

Кроме того, раз Яндекс за 3 года не сподобился придумать новый проект, претензии ревьюеров, для улучшения проекта, можно записывать сюда: [Вопросы](https://github.com/Xewus/foodgram-project-react/issues).

Имейте ввиду, что некоторые ревьюры сами не сильно углублялись в предмет, проверку проводят сравнивая с выданным им шаблоном и иногда их претензии решаются не переписыванием кода, а объяснением Вашего решения. Не стесняйтесь спорить с ними. 
***

## Tecnhologies:
- Python 3.10
- Django 4.0
- Django REST framework 3.13
- Nginx
- Docker
- Postgres


## https://foodgram.gq


Here you can share recipes of dishes, add them to favorites and display a shopping list for cooking your favorite dishes.
To preserve order - only administrators are allowed to create tags and ingredients.

There is also an API. To view the available paths, follow the link: **https://foodgram.gq/api/**.

And the api documentation is here: **https://foodgram.gq/api/redoc/**.

### To deploy this project need the next actions:
- Download project with SSH (actually you only need the folder 'infra/')
```
git clone git@github.com:Xewus/foodgram-project-react.git
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
ALLOWED_HOSTS=<Your_host>
CSRF_TRUSTED_ORIGINS=https://<Your_host>
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

Oh, I'm sorry. You also need to create the first account for the admin panel using this command:
```
sudo docker exec -it app python manage.py createsuperuser
```

And if you want, you can use the list of ingredients offered by us to write
recipes.
Upload it to the database with the following command:
```
sudo docker exec -it app python manage.py loaddata data/dump.json
```

### *Backend by:*
[Xewus](https://github.com/Xewus)
