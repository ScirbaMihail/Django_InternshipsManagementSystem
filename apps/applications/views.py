from rest_framework.viewsets import ModelViewSet

from apps.applications.models import Application
from apps.applications.serializers import ApplicationSerializer


class ApplicationViewSet(ModelViewSet):
    queryset = Application
    serializer_class = ApplicationSerializer
    http_method_names = ['get', 'head', 'post']
