from rest_framework import serializers

from apps.users import models as user_models


class UserModelSerializer(serializers.ModelSerializer):

    today_calorie_sum = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    current_month_price_sum = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = user_models.User
        fields = [
            'user_id', 'first_name', 'last_name', 'role',
            'daily_calorie_threshold', 'monthly_price_threshold',
            'today_calorie_sum', 'current_month_price_sum'
        ]
