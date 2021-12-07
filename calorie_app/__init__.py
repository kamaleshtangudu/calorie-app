from .celery_app import app as celery_app  # pylint: disable=E0401

__all__ = ('celery_app',)