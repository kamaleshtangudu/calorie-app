# from django.db.models import Q
# from django_filters.rest_framework import DateFilter, FilterSet

# from apps.food import models as food_models


# class MedicationFilter(FilterSet):
#     end_date = DateFilter(field_name='taken_at', lookup_expr='lte')
#     start_date = DateFilter(method='filter_medication_by_end')

#     def filter_medication_by_end(self, queryset, name, value):
#         if value:
#             return queryset.filter(Q(end_date__isnull=True) | Q(end_date__gte=value))
#         return queryset

#     class Meta:
#         model = food_models.Food
#         fields = ['start_date', 'end_date']
