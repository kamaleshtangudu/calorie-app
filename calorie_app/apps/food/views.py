import datetime
import pytz

from django.conf import settings
from django.db.models import Sum, FloatField, Value
from django.db.models.functions import Cast, Coalesce, Trunc
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.base.view_mixins import CurrentUserQuerySetMixin, MultiplePermissionMixin, MultipleSerializerMixin
from apps.food import models as food_models, serializers as food_serializers
from apps.users.permissions import IsAdmin
from apps.users import models as user_models


class FoodViewSet(CurrentUserQuerySetMixin, MultiplePermissionMixin, MultipleSerializerMixin, viewsets.ModelViewSet):

    http_method_names = ['get', 'post', 'patch', 'delete']

    serializer_class = food_serializers.FoodModelSerializer

    queryset = food_models.Food.objects.select_related('user').all().order_by('-taken_at')

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]

    filterset_fields = {
        'user': ['exact'],
        'taken_at': ['gte', 'lte', 'date__range', 'gt', 'lt']
    }

    search_fields = ['name']

    ordering_fields = ['name', 'taken_at', 'calories', 'price']

    def get_queryset(self):

        queryset = super().get_queryset()

        # Admins can ask food of any user, if not provided we fallback to the current user(admin itself)
        # Normal users cannot ask for other user, because the data is already filtered wrt to their accessible rows
        if not self.request.query_params.get('user') and self.action == 'list':
            queryset = queryset.filter(user=self.request.user)

        return queryset


class ReportViewSet(viewsets.GenericViewSet):

    queryset = food_models.Food.objects.all()

    http_method_names = ['get']

    permission_classes = [IsAuthenticated, IsAdmin]

    serializer_class = food_serializers.ReportSerializer

    @action(methods=['get'], detail=False, pagination_class=None)
    def report(self, request):
        start_time_of_the_week = datetime.datetime.combine(
            (timezone.now() - datetime.timedelta(days=6)).date(),
            datetime.time.min
        )

        start_time_of_last_week = datetime.datetime.combine(
            (timezone.now() - datetime.timedelta(days=13)).date(),
            datetime.time.min
        )

        food_count_of_the_week = food_models.Food.objects.filter(taken_at__gte=start_time_of_the_week).count()

        food_count_of_last_week = food_models.Food.objects.filter(
            taken_at__lt=start_time_of_the_week, taken_at__gte=start_time_of_last_week
        ).count()

        users_count = user_models.User.objects.all().count()

        avg_per_user_per_day_calories = food_models.Food.objects.filter(
            taken_at__gte=start_time_of_the_week
        ).aggregate(
            avg_per_user_per_day_calories=Coalesce(
                Cast(Sum('calories'), FloatField()) / (users_count * 7),
                Value(0)
            )
        )['avg_per_user_per_day_calories']

        return Response({
            'food_count_of_the_week': food_count_of_the_week,
            'food_count_of_last_week': food_count_of_last_week,
            'avg_per_user_per_day_calories': round(avg_per_user_per_day_calories, 2)
        })


class ThresholdViewSet(CurrentUserQuerySetMixin, viewsets.GenericViewSet):

    queryset = food_models.Food.objects.all()

    http_method_names = ['get']

    serializer_class = food_serializers.ThresholdSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_fields = {
        'user': ['exact'],
        'taken_at': ['gte', 'lte', 'date__range', 'gt', 'lt']
    }

    @action(methods=['get'], detail=False, pagination_class=None)
    def threshold(self, request):

        queryset = self.filter_queryset(self.get_queryset())

        # Admins can ask thresholds of any user, if not provided we fallback to the current user(admin itself)
        # Normal users cannot ask for other user, because the data is already filtered wrt to their accessible rows
        query_user = request.query_params.get('user')
        if not query_user:
            query_user = request.user
            queryset = queryset.filter(user=request.user)
        else:
            # If admin asks data of different user, we retrieve the user
            # to verify calories taken on a day against his threshold
            query_user = user_models.User.objects.filter(user_id=query_user).first()

        calorie_queryset = (
            queryset
            .annotate(
                record_date=Trunc(
                    'taken_at',
                    'day',
                    tzinfo=pytz.timezone(settings.TIME_ZONE)
                )
            )
            .values('record_date')
            .annotate(calorie_sum=Coalesce(Sum('calories'), Value(0)))
            .values('record_date', 'calorie_sum')
            .order_by('-record_date')
        )

        price_queryset = (
            queryset
            .annotate(
                record_month=Trunc(
                    'taken_at',
                    'month',
                    tzinfo=pytz.timezone(settings.TIME_ZONE)
                )
            )
            .values('record_month')
            .annotate(price_sum=Coalesce(Sum('price'), Value(0)))
            .values('record_month', 'price_sum')
            .order_by('-record_month')
        )

        return Response({'results': {
            'calorie_thresholds': [
                record['record_date'].date().isoformat()
                for record in list(calorie_queryset)
                if record['calorie_sum'] > query_user.daily_calorie_threshold
            ],
            'price_thresholds': {
                record['record_month'].date().isoformat()
                for record in list(price_queryset)
                if record['price_sum'] > query_user.monthly_price_threshold
            }
        }})
