coverage run --source='.' manage.py test
coverage report --omit='conf.py','winparf/__init__.py','winparf/wsgi.py'
