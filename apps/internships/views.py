from rest_framework.viewsets import ModelViewSet

from apps.internships.models import Internship
from apps.internships.serializers import InternshipSerializer


class InternshipViewSet(ModelViewSet):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    http_method_names = ['get', 'head']