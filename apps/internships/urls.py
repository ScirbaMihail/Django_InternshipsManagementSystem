from rest_framework.routers import DefaultRouter

from apps.internships.views import InternshipViewSet

router = DefaultRouter()
router.register(r'internships', InternshipViewSet, basename='internships')
urlpatterns = router.urls
