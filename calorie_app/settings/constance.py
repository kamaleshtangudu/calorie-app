from collections import OrderedDict


class LiveSettingsMixin:
    """
    Contains All Live-settings variable in one place
    """

    # Constance Variables
    CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
    CONSTANCE_DATABASE_CACHE_BACKEND = 'default'

    CONSTANCE_ADDITIONAL_FIELDS = {
        'json': [
            'django.contrib.postgres.forms.JSONField', {
                'widget': 'django_json_widget.widgets.JSONEditorWidget'
            }
        ],
        'password_field': [
            'django.forms.fields.CharField', {
                'widget': 'django.forms.PasswordInput',
                'widget_kwargs': {"render_value": True}
            }
        ]
    }

    CONSTANCE_CONFIG = {}

    CONSTANCE_CONFIG_FIELDSETS = OrderedDict([("General", []),])