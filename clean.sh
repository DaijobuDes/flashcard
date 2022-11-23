rm -rfv api/migrations/
rm -rfv lexicard_web/migrations/
rm -v db.sqlite3

python3 ./manage.py makemigrations lexicard_web
python3 ./manage.py migrate

python3 ./manage.py runserver