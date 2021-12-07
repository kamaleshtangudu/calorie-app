import datetime

from django.db.models import Sum, Q, Value
from django.db.models.functions import Coalesce
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters

from apps.base.view_mixins import CurrentUserQuerySetMixin
from apps.users import models as user_models, serializers as user_serializers


class UserViewSet(CurrentUserQuerySetMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    serializer_class = user_serializers.UserModelSerializer

    http_method_names = ['get']

    queryset = user_models.User.objects.all()

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]

    filterset_fields = ['role']

    search_fields = ['first_name', 'last_name']

    ordering_fields = ['daily_calorie_threshold', 'monthly_price_threshold']

    def get_queryset(self):
        queryset = super().get_queryset()

        today_start_time = datetime.datetime.combine(
            timezone.now().date(), datetime.time.min
        )

        current_month_start_time = datetime.datetime.combine(
            timezone.now().date().replace(day=1), datetime.time.min
        )

        return queryset.annotate(
            today_calorie_sum=Coalesce(
                Sum(
                    'my_foods__calories',
                    filter=Q(
                        my_foods__taken_at__gte=today_start_time
                    )
                ),
                Value(0)
            ),
            current_month_price_sum=Coalesce(
                Sum(
                    'my_foods__price',
                    filter=Q(
                        my_foods__taken_at__gte=current_month_start_time
                    )
                ),
                Value(0)
            )
        )
