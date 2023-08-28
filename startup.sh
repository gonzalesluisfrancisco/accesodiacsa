python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
gunicorn --bind=0.0.0.0 --timeout 600 controlaesadiacsa.wsgi
