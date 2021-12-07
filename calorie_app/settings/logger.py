from os.path import dirname, abspath, join, exists
import os


class LoggerSettingsMixin:
    """
    Log Settings Mixin
    """

    # log_dir = os.environ.get("LOG_DIR")

    # if not log_dir:
    #     # Create a local log directory if one is not defined
    #     root = dirname(dirname(dirname(abspath(__file__))))
    #     log_dir = join(root, 'logs')
    #     if not exists(log_dir):
    #         os.makedirs(log_dir)

    # log_file_name = join(log_dir, 'apis.log')
    # error_log_file_name = join(log_dir, 'error.log')

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            }
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue'
            }
        },
        'handlers': {
            'null': {
                'level': 'INFO',
                'class': 'logging.NullHandler',
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'filters': ['require_debug_true'],
                'formatter': 'verbose'
            },
            'error_console': {              # To track the traceback
                'level': 'ERROR',
                'class': 'logging.StreamHandler',
                'filters': ['require_debug_true'],
                'formatter': 'verbose'
            },
            # 'sentry': {
            #     'level': 'ERROR',
            #     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            # },
            # # Storage log may be later sent to Centralized logging system
            # 'storage': {
            #     'level': 'DEBUG',
            #     'class': 'logging.handlers.RotatingFileHandler',
            #     'filename': log_file_name,
            #     'maxBytes': 1024 * 1024 * 1,  # 1 MB
            #     'backupCount': 4,
            #     'formatter': 'verbose'
            # },
            # # Storage log may be later sent to Centralized logging system
            # 'error_storage': {
            #     'level': 'ERROR',
            #     'class': 'logging.handlers.RotatingFileHandler',
            #     'filename': error_log_file_name,
            #     'maxBytes': 1024 * 1024 * 1,  # 1 MB
            #     'backupCount': 4,
            #     'formatter': 'verbose'
            # }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins', 'console'],
                'level': 'INFO',
                'propagate': True,
            },
            'django': {
                'handlers': ['console', 'error_console'],
                'level': 'INFO',
                'propagate': False,
            },
            'apps': {
                'handlers': ['console', 'error_console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            # Catch All Logger -- Captures any other logging
            '': {
                'handlers': ['console', 'error_console'],
                'level': 'INFO',
                'propagate': False,
            }
        }
    }