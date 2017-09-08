# Lincoln Pokemon GO Map Stats

## Getting Started

1. Install nodejs and npm

2. Symlink node to nodejs

```bash
ln -s /usr/bin/nodejs /usr/bin/node
```

3. Install bower components

```bash
npm install -g bower
cd assets
bower install
```

4. Set up your python environment and run

```bash
virtualenv venv -p python3
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Local Settings

You should probably overwrite the `DATABASES` setting in your `viper/local.py`. Here's an example.

```python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bulu',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Note: Before production, `DEBUG`, `SECRET_KEY`, and `ALLOWED_HOSTS` should also be overwritten.

## Running Tests

To run tests, simply run `runtests.sh`
