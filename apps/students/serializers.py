from rest_framework.serializers import ModelSerializer

from apps.students.models import Student

class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        extra_kwargs = {
            'idnp': {'validators': []},
            'email': {'validators': []},
            'phone_number': {'validators': []},
        }