from django.urls import path
from rest_framework.routers import DefaultRouter


from apps.companies.views import CompanyViewSet

# register routers for api
router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='companies')

urlpatterns = router.urls
