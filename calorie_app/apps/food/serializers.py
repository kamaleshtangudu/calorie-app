from rest_framework import serializers

from apps.users import (
    serializers as user_serializers,
    models as user_models,
    constants as user_constants
)
from apps.food import models as food_models


class FoodModelSerializer(serializers.ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    user = user_serializers.UserModelSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=user_models.User.objects.all(), source='user', write_only=True
    )

    def validate_user_id(self, value):
        if (
            value
            and value != self.context['request'].user
            and self.context['request'].user.role != user_constants.UserRoles.ADMIN
        ):
            raise serializers.ValidationError('Non Admin users can add food only for themselves')

        return value

    class Meta:
        model = food_models.Food
        fields = [
            'id', 'name', 'user', 'user_id', 'taken_at', 'calories', 'price',
            'created_by', 'updated_by', 'created_at', 'updated_at'
        ]


class ReportSerializer(serializers.Serializer):

    food_count_of_the_week = serializers.IntegerField()
    food_count_of_last_week = serializers.IntegerField()
    avg_per_user_per_day_calories = serializers.DecimalField(max_digits=10, decimal_places=2)


class ThresholdsSerializer(serializers.Serializer):

    calorie_thresholds = serializers.ListField(child=serializers.DateField())
    price_thresholds = serializers.ListField(child=serializers.DateField())


class ThresholdSerializer(serializers.Serializer):

    results = ThresholdsSerializer()
