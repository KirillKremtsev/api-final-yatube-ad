# api_final
api final
# API для Yatube

Социальная сеть для публикации личных дневников.  
REST API позволяет управлять постами, комментариями, группами и подписками.

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
git clone https://github.com/KirillKremtsev/api-final-yatube-ad.git
cd api-final-yatube-ad/yatube_api

Создать и активировать виртуальное окружение:
python -m venv venv
source venv/bin/activate # для Linux/Mac

или для Windows:
venv\Scripts\activate

Установить зависимости из файла requirements.txt:
python -m pip install --upgrade pip
pip install -r requirements.txt

Выполнить миграции:
python manage.py migrate

Запустить проект:
python manage.py runserver

## Примеры запросов к API

### Получение списка постов (доступно без токена)
GET /api/v1/posts/

### Создание нового поста (требуется JWT-токен)
POST /api/v1/posts/
Authorization: Bearer <ваш_access_токен>
Content-Type: application/json

{
"text": "Мой первый пост",
"group": 1
}

### Получение списка подписок (только авторизованные)
GET /api/v1/follow/
Authorization: Bearer <ваш_access_токен>

### Подписка на пользователя
POST /api/v1/follow/
Authorization: Bearer <ваш_access_токен>
Content-Type: application/json

{
"following": "username"
}

### Получение комментариев к посту
GET /api/v1/posts/1/comments/

### Добавление комментария
POST /api/v1/posts/1/comments/
Authorization: Bearer <ваш_access_токен>
Content-Type: application/json

{
"text": "Отличный пост!"
}

## Документация

После запуска сервера документация в формате ReDoc доступна по адресу:  
`http://127.0.0.1:8000/redoc/`