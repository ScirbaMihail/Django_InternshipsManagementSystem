from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.applications.views import ApplicationViewSet, ProtectedView

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='applications')
urlpatterns = (router.urls + [
    path('protected/', ProtectedView.as_view(), name='protected'),
])
