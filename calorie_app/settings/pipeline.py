import os
import random
import string

from . import common  # pylint: disable=E0401


class Settings(common.Settings):

    # Generate a secret key for ci tasks like collectstatic etc
    SECRET_KEY = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(32))

    ENVIRONMENT_CODE = os.environ.get('ENVIRONMENT_CODE', 'pipeline')

    common.Settings.CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        "KEY_PREFIX": "calorie_app_test"
    }

    CONSTANCE_DBS = ['default']
    CONSTANCE_BACKEND = 'constance.backends.memory.MemoryBackend'
