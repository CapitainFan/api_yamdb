# api_yamdb

### Описание
Это командный проект, по курсу яндекс-практикум, в котором пользователь может зарегестрироваться, писать свои отзывы и коментарии, читать чужие и находить новые произведения.

### Технологии
Python 3.7  - https://docs.python.org/release/3.7.0/;  
Django 2.2.19 - https://docs.djangoproject.com/en/4.1/ ;  
API - https://docs.python.org/release/3.7.0/distutils/apiref.html?highlight=api;  
DRF - https://www.django-rest-framework.org/  

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:CapitainFan/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
cd api_yamdb
```

```
python manage.py makemigrations
```

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### Примеры запросов

В проекте доступны следующие эндпоинты:

```
http://127.0.0.1:8000/api/v1/auth/signup/  - Получение кода подверждения на email
```

{
"email": "string",
"username": "string"
}

```
http://127.0.0.1:8000/api/v1/auth/token/ - Получение токена для авторизации
```

{
"username": "string",
"confirmation_code": "string"
}

```
http://127.0.0.1:8000/api/v1/categories/ - Работа с категориями, доступны запросы Get, Post и Del
```

```
http://127.0.0.1:8000/api/v1/genres/ - Работа с жанрами, доступны запросы Get, Post и Del
```

```
http://127.0.0.1:8000/api/v1/titles/ - Работа со статьями , доступны запросы Get, Post, Patch и Del
```

```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/  - Работа с отзывами , доступны запросы Get, Post, Patch и Del
```

```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Работа с комментариями , доступны запросы Get, Post, Patch и Del
```

```
http://127.0.0.1:8000/api/v1/users/ - Создание пользователя и получение информации о всех пользователях. Доступны запросы Get, Post
```

```
http://127.0.0.1:8000/api/v1/users/{username}/ - Получение информации о конкретном пользователе и редактирование информации о нем. Доступны доступны запросы Get, Postm Del
```

```
http://127.0.0.1:8000/api/v1/users/me/ - Получение и изменение своих данных, доступны запросы Get, Patch
```

### Авторы
1. Auth/Users - Мухамеджанова Дарья Сергеевна,
2. Categories/Genres/Titles - Перепелкин Александр,
3. Review/Comments - Никита Гудков
