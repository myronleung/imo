web: python manage.py runserver 0.0.0.0:$PORT
web: python imo/imo_app/manage.py collectstatic --noinput; bin/gunicorn_django --workers=4 --bind=0.0.0.0:$PORT imo/imo/settings.py
