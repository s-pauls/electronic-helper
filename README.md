# Church Management
Этот проект создан для поддержки организационных процессов в церкви. 
В проекте используется фреймворк [DJANGO](https://djbook.ru/rel3.0/).

## Локальное разворачивание и запуск

Для работы с проктом нужно:
- Скачать и установить [Python](https://www.python.org/ftp/python/3.7.4/python-3.7.4-amd64.exe) _(на хостинге используется версия 3.6.9)_ 
  - ! во время установки нужно включить галочку Add Python to environment variables !
- Скачать и установить [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows)
- Скачать и установить [MySql](https://dev.mysql.com/downloads/file/?id=510039)
  - ! во время установки выбрать опцию Use Legacy Authentication Method (Retain MySQL 5.x Compatibility)
    (на серевере используется MySQL 5.7)
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
для добавдления (инициализации задач нужно вызвать [run_jobs()](church_app/main/tasks.py))
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
Проет имеет несколько презентационных уровней
- Веб-интерфейс [templates](church_app/main/templates)
- АПИ [api](church_app/main/api)
- Фоновые процессы [jobs](church_app/main/jobs)

Все "головы" проекта используют бизнеслогику [core](church_app/main/core) для выполнения своих задач 

## Используемые переменные среды:
Тут перечисленны переменные и их описание, которые используются в проекте 

| Переменная               | Описание                                                     |
|--------------------------|--------------------------------------------------------------|
| DJANGO_DEBUG             | True/False - во время разработки нужно установить True       |
| DJANGO_ALLOWED_HOSTS     | разрешенные хосты. *                                         |
| DJANGO_SECRET_KEY        | секретный ключ, который нужен для шифрования cookie          |   
| DJANGO_LOG_LEVEL         | DEBUG, INFO, WARNING, ERROR, CRITICAL - уровень логгирования |
| DJANGO_LOG_DIRECTORY     | Папка, куда будут писаться логи                              |
| MYSQL_NAME               | Имя базы данных                                              |
| MYSQL_USER               | Имя пользователя базы данных                                 |
| MYSQL_PASS               | Пароль для доступа к базе данных                             |
| NOTION_TOKEN             | токен доступа к церковному Notion                            |
| NOTION_RU_WORSHIP_TOKEN  | токен доступа к RuWorship Notion                             |
| VK_RU_WORSHIP_TOKEN      | токен доступа к RuWorship vk.com                             |
| VK_GOMEL_GRACE_LOGIN     | номер телефона для входа в VK                                |
| VK_GOMEL_GRACE_PASSWORD  | пароль для входа в VK                                        |
| TRELLO_API_KEY           | Секрет Trello                                                | 
| TRELLO_API_SECRET        | Секрет Trello                                                |
| TRELLO_TOKEN             | Секрет Trello                                                |
| TRELLO_TOKEN_SECRET      | Секрет Trello                                                |

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


---

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/gomelgrace/church-management.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.com/gomelgrace/church-management/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Automatically merge when pipeline succeeds](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!).  Thank you to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README
Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
