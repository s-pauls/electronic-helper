# Church Management
Этот проект создан для поддержки организационных процессов в церкви. 
В проекте используется фреймворк [DJANGO](https://djbook.ru/rel3.0/).

![](documentation/Data%20Flow%20Diagram.drawio.svg)

[Data Flow Diagram](documentation/Data%20Flow%20Diagram.html)

## Локальное разворачивание и запуск

Для работы с проектом нужно:
- Скачать и установить [Python](https://www.python.org/ftp/python/3.7.4/python-3.7.4-amd64.exe) _(на хостинге используется версия 3.6.9)_ 
  - ! во время установки нужно включить галочку Add Python to environment variables !
- Скачать и установить [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows)
- Скачать и установить [MySql](https://dev.mysql.com/downloads/file/?id=510039)
  - ! во время установки выбрать опцию Use Legacy Authentication Method (Retain MySQL 5.x Compatibility)
    (на сервере используется MySQL 5.7)
  - Создать схему в базе CREATE SCHEMA `church_management` DEFAULT CHARACTER SET utf8 ;
  - Рекомендую использовать DBeaver вместо MySQL Workbanch для просмотра содержимого в базе
- Создать файл .env в папке church_app со следующим содержимым
```
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_SECRET_KEY=cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag
DJANGO_LOG_LEVEL=DEBUG
DJANGO_LOG_DIRECTORY=logs
MYSQL_NAME=church_management
MYSQL_USER=root
MYSQL_PASS=root
NOTION_TOKEN=
NOTION_RU_WORSHIP_TOKEN=
VK_RU_WORSHIP_TOKEN=
VK_GOMEL_GRACE_LOGIN=
VK_GOMEL_GRACE_PASSWORD=
TRELLO_API_KEY=
TRELLO_API_SECRET=
TRELLO_TOKEN=
TRELLO_TOKEN_SECRET=
VIBER_ACCESS_TOKEN=
```
- Создать папку logs для логов в папке church_app
- Для установки зависимостей запустить команду 
```bash
pip install -r requirements.txt
```

Для запуска проекта в терминале выполняем команду: 
для перехода из папки church-management в папку, где есть manage.py
```bash
cd church_app
```

запуск проекта
```bash
python manage.py runserver
```

запуск фоновых задач 
задачи должны быть добавлены в таблице background_task
для добавления (инициализации задач нужно вызвать [run_jobs()](church_app/main/tasks.py))
```bash
python manage.py process_tasks
```

для останова проекта достаточно в терминале нажать Ctrl+C

## Структура проекта
Проект создан с помощью DJANGO 

```bash
django-admin startproject church_app)
``` 
church_app - это корневая папка проекта

В проект добален один Application - **main**
```commandline
python manage.py startapp main
```
в нем будем располагать нашу логику сайта и АПИ

### Бизнес логика проекта
Вся логика проекта должна находиться в пакете [core](church_app/main/core)

### Презентационный уровень проекта
Проект имеет несколько презентационных уровней
- Веб-интерфейс [templates](church_app/main/templates)
- АПИ [api](church_app/main/api)
- Фоновые процессы [jobs](church_app/main/jobs)

Все "головы" проекта используют бизнеслогику [core](church_app/main/core) для выполнения своих задач 

## Используемые переменные среды:
Тут перечисленны переменные и их описание, которые используются в проекте 

| Переменная              | Описание                                                     |
|-------------------------|--------------------------------------------------------------|
| DJANGO_DEBUG            | True/False - во время разработки нужно установить True       |
| DJANGO_ALLOWED_HOSTS    | разрешенные хосты. *                                         |
| DJANGO_SECRET_KEY       | секретный ключ, который нужен для шифрования cookie          |   
| DJANGO_LOG_LEVEL        | DEBUG, INFO, WARNING, ERROR, CRITICAL - уровень логгирования |
| DJANGO_LOG_DIRECTORY    | Папка, куда будут писаться логи                              |
| MYSQL_NAME              | Имя базы данных                                              |
| MYSQL_USER              | Имя пользователя базы данных                                 |
| MYSQL_PASS              | Пароль для доступа к базе данных                             |
| NOTION_TOKEN            | токен доступа к церковному Notion                            |
| NOTION_RU_WORSHIP_TOKEN | токен доступа к RuWorship Notion                             |
| VK_RU_WORSHIP_TOKEN     | токен доступа к RuWorship vk.com                             |
| VK_GOMEL_GRACE_LOGIN    | номер телефона для входа в VK                                |
| VK_GOMEL_GRACE_PASSWORD | пароль для входа в VK                                        |
| TRELLO_API_KEY          | Секрет Trello                                                | 
| TRELLO_API_SECRET       | Секрет Trello                                                |
| TRELLO_TOKEN            | Секрет Trello                                                |
| TRELLO_TOKEN_SECRET     | Секрет Trello                                                |
| VIBER_ACCESS_TOKEN      | Токен доступа к Viber - боту                                 |

## Гит flow
Основная ветка **main**. Из нее код попадает на хостинг (продакшн). Коммитить сразу в main запрещено. 
Под каждую задачу нужно создавать отдельную ветку от **свежего**  main. 
Когда код отлажен локально нужно push-нуть ее на gitlab и создать Merge Request (Запрос на объединение с main веткой). 
Право объединения на текущий момент имеют пользователи с ролью Maintainer

## Environment variables flow
**В целях безопасности токены, пароли и другие важные параметры не должны быть в коде!**
Решено хранить их в отдельном репозитории CONFIGURATION. При необходимости добавить новую настройку нужно:
- добавить описание переменной в этот файл в секцию "Используемые переменные среды"
- сообщить о необходимости добавления переменной в CONFIGURATION-репозиторий (просьбу о добавлении можно оставить прямо в описании Merge Request)

## Полезные ссылки
- [Работа с базой](https://docs.djangoproject.com/en/1.8/ref/models/querysets/#update)
- [Доска с задачами](https://trello.com/invite/b/n8ByXxI3/1338e3daaaada097be692b208a70ea99/%D0%B2%D0%B5%D0%B1-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5) 
