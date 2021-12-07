from django.db import models

from apps.base.models import BaseModel
from apps.users import constants as user_constants


class User(BaseModel):

    user_id = models.CharField(
        max_length=50,
        primary_key=True,
        help_text='Would also act as token for the assignment'
    )

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    daily_calorie_threshold = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=2100,
        help_text='Calorie limit per day as set by the user, units is Cal.'
    )

    daily_price_threshold = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=1000,
        help_text='Price limit per day as set by the user, units is USD.'
    )

    role = models.CharField(
        max_length=25,
        choices=user_constants.UserRoles,
    )

    @property
    def is_authenticated(self):
        return True
