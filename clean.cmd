del /S /F /Q api\migrations\
del /S /F /Q lexicard_web\migrations\
del /F db.sqlite3

py manage.py makemigrations lexicard_web
py manage.py migrate

py manage.py runserver