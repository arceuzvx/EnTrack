web: gunicorn entrack.wsgi
release: python manage.py migrate && python create_superuser.py
