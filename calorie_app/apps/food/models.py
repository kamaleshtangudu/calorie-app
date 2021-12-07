from django.db import models
from django.utils import timezone

from apps.base.models import BaseModel
from apps.users.models import User


class Food(BaseModel):

    name = models.CharField(max_length=100)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='my_foods',
    )

    calories = models.DecimalField(
        decimal_places=2,
        max_digits=10,
    )

    price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
    )

    taken_at = models.DateTimeField(default=timezone.now)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='my_created_foods',
        null=True
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='my_updated_foods',
        null=True
    )
