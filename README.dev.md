## Poetry Init
```bash
poetry install
poetry show --tree
```

## RUN Local (windows)
```bash
.venv\Scripts\activate
cd src
py manage.py runserver 0.0.0.0:8030
```

## RUN Celery workers for email sending (if we have redis http://localhost:6379/)
```bash
.venv\Scripts\activate
cd src
celery -A core.celery worker --pool=solo --loglevel=info
```

## RUN Docker
```bash

# Run containers
.venv\Scripts\activate
docker-compose up --build

# Delete containers
docker-compose down -v
```

## RUN Tests
```bash
cd src
py manage.py test
```

## VS Code plugins
```
Python, Pylance, Black Formatter, autopep8
```

## django-extensions commands
```bash
py manage.py runserver_plus 8030
py manage.py generate_secret_key
py manage.py show_urls
```
