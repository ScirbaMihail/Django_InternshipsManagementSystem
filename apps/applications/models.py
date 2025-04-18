from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.internships.models import Internship
from apps.students.models import Student


class Application(models.Model):
    class Status(models.TextChoices):
        APPROVED = 'app', _('Approved')
        REJECTED = 'rej', _('Rejected')
        IN_PROGRESS = 'prg', _('In progress')

    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='student_idnp')
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.IN_PROGRESS)

    def get_status(self) -> Status:
        return self.Status(self.status)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'internship'],
                name='unique_student_internship'
            )
        ]
        db_table = 'applications'

    def __str__(self):
        return f'{self.student} at {self.internship}, {self.status}'