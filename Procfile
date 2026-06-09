web: cd frontend && npm install && npm run build && cd .. && python manage.py migrate && python manage.py seed && python manage.py collectstatic --noinput && gunicorn think_tank.wsgi
