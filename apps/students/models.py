from django.db import models

class Student(models.Model):
    idnp = models.CharField(primary_key=True, max_length=13)
    first_name = models.CharField(null=False)
    last_name = models.CharField(null=False)
    address = models.CharField(null=False)
    email = models.EmailField(default=None, blank=True, null=True, unique=True)
    phone_number = models.CharField(null=False, unique=True)

    class Meta:
        db_table = 'students'