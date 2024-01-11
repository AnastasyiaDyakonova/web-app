Инструкция по установке:
У вас уже должен быть установлен postgresql, DBeaver, PyCharm, git, python
В postgresql нужно создать базу данных и назвать ее "mysite".
В той папке, в которой ходим соханить проект открываем Git Bash и вводим команду git clone https://github.com/AnastasyiaDyakonova/web-app.git.
Должен появиться проект в этой папке.
Далее открываем PyCharm, нажимаем на File -> Open, выбираем путь к приложению. Нажимаем ок -> This Window. Должен открыться скелет проекта.
Нажимаем на alt+f12, должно открыться внизу окно терминала. Проверьте Ваш путь. Должен заканчиваться на \web-app>
Далее вводим команду:
python -m venv venv
Она создает виртуальное окружение проекта. В скелете приложения должна появиться папка venv.
Далее в терминале вводим команды:
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirement.txt
pip install django

Далее перейдите в папку mysite/mysite и откройте файл settings.py. В этом блоке:
DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql",
        'NAME': 'mysite',
        "USER": "postgres",
        "PASSWORD": "******",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
исправьте пароль(Вы его создавали после установки postgres) и порт на Ваш. Сохраните файл.


Вернемся в терминал и пропишем следующие команды:
 cd mysite
 python manage.py makemigrations
 python manage.py migrate
 python manage.py runserver

После последней команды должно получиться:
System check identified 1 issue (0 silenced).
January 12, 2024 - 00:48:19
Django version 5.0, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

Переходим по ссылке http://127.0.0.1:8000/ и тестим.

