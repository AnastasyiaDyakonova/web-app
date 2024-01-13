Инструкция по установке:
У вас уже должен быть установлен Oracle(он на стороне клиента), DBeaver, PyCharm, git, python(версия 3.9)
Переходим по ссылке https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html
Скачиваем последнюю версию в виде архива. Архив распаковываем, папку instantclient_21_12 можно разместить по такому пути на вашем ПК(можно и свой задать-путь к этой папке понадобится далее):
C:\Program Files\Oracle\instantclient_21_12
Теперь нам нужно добавить этот адрес в переменные среды на ПК. У меня такой порядок действий был:
нажимаю на "Этот компьютер" правой кнопкой мыши, выбираю "свойства", далее "Дополнительные параметры системы", далее "переменные среды".
В "Системные переменные" есть "Path", кликаю на него, "создать", добавляю адрес - у меня это C:\Program Files\Oracle\instantclient_21_12. Далее два раза ок.


В той папке, в которой ходим соханить проект открываем Git Bash и вводим команду git clone https://github.com/AnastasyiaDyakonova/web-app.git.
Должен появиться проект в этой папке.
Далее открываем PyCharm, нажимаем на File -> Open, выбираем путь к приложению. Нажимаем ок -> This Window. Должен открыться скелет проекта.
Нажимаем на alt+f12, должно открыться внизу окно терминала. Проверьте Ваш путь. Должен заканчиваться на \web-app>
Вводим команды:
python -m pip install cx_Oracle --upgrade
pip install sqlalchemy
pip install pandas
Далее вводим команду:
python -m venv venv
Она создает виртуальное окружение проекта. В скелете приложения должна появиться папка venv.
Далее в терминале вводим команды:
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirement.txt
pip install django

Далее перейдите в папку mysite и откройте файл manage.py. В этом блоке:
lib_dir = r"C:\Program Files\Oracle\instantclient_21_12"
замените на Ваш путь instantclient_21_12


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

