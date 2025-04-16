from rest_framework.viewsets import ModelViewSet

from apps.companies.models import Company
from apps.companies.serializers import CompanySerializer

class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    http_method_names = ['get', 'head']