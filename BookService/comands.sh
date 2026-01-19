
python manage.py migrate --noinput
gunicorn --bind 0.0.0.0:800 BookService.wsgi:application