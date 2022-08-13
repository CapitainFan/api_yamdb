# api_yamdb

### Описание
Это командный проект, по курсу яндекс-практикум, в котором пользователь может зарегестрироваться, писать свои отзывы и коментарии, читать чужие и находить новые произведения.

### Технологии
Python 3.7 ;  
Django 2.2.19 ;  
API

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

### Авторы
1. Auth/Users - Мухамеджанова Дарья Сергеевна,
2. Categories/Genres/Titles - Перепелкин Александр,
3. Review/Comments - Никита Гудков
