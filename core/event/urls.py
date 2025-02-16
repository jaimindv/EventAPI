from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventViewset

router = DefaultRouter()

router.register("", EventViewset, basename="events")

urlpatterns = [
    path("", include(router.urls)),
]
