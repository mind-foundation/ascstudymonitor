""" Tasks for celery """
from celery import Celery

from .app import app
from .config import asc_celery_broker, tweets_from


def make_celery(app):
    celery = Celery(app.import_name, broker=asc_celery_broker)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)
