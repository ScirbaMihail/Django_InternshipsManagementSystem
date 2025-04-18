from rest_framework import serializers

from apps.applications.models import Application
from apps.students.models import Student
from apps.students.serializers import StudentSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=False, required=True)

    class Meta:
        model = Application
        fields = '__all__'

    def create(self, validated_data):
        student_data = validated_data.pop('student')
        student_idnp = student_data['idnp']
        student, created = Student.objects.get_or_create(
            idnp=student_idnp,
            defaults=student_data
        )
        application = Application.objects.create(
            student=student,
            **validated_data
        )
        return application
