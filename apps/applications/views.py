from django.dispatch import receiver
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.applications.models import Application
from apps.applications.serializers import ApplicationSerializer
from apps.applications.tasks import send_notification
from apps.internships.models import Internship
from apps.students.models import Student


class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    http_method_names = ['get', 'head', 'post', 'put']

    def perform_update(self, serializer):
        prev_status = serializer.instance.status
        super().perform_update(serializer)
        current_status = serializer.data['status']
        if prev_status != current_status and current_status in [Application.Status.APPROVED, Application.Status.REJECTED]:
            internship = Internship.objects.get(pk=serializer.data['internship'])
            company = internship.company
            student = serializer.data['student']
            send_notification(
                company_name = company.name,
                company_mail = company.email,
                student_name = f'{student["first_name"]} {student["last_name"]}',
                student_mail = student['email'],
                internship_title = internship.name,
                internship_status=current_status,
            )

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1MzMyNjU3LCJpYXQiOjE3NDUzMjkwNTcsImp0aSI6ImRkNjIzZDliMWU2NjQ0ZjA5MTgyNDg5ODYzMjY2N2QxIiwidXNlcl9pZCI6MX0.Cq5fK4T7sIcLGf-LC6fXtf7VCk3EBBgeKAOTjts4PDs


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This view is protected"})