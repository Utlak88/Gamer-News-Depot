release: python manage.py migrate
web: gunicorn news.wsgi --preload --log-file -
worker: celery -A news worker -l INFO
beat: celery -A news beat -l INFO -S redbeat.RedBeatScheduler