from rest_framework.routers import DefaultRouter

from apps.applications.views import ApplicationViewSet

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='applications')
urlpatterns = router.urls
