from rest_framework import routers

from apps.food.views import FoodViewSet, ReportViewSet, ThresholdViewSet

router = routers.SimpleRouter()
router.register(r'food', FoodViewSet)
router.register(r'', ReportViewSet)
router.register(r'', ThresholdViewSet)

urlpatterns = []
urlpatterns += router.urls
