from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.students.models import Student
from apps.internships.models import Internship


class Application(models.Model):
    class Status(models.TextChoices):
        APPROVED = 'app', _('Approved')
        REJECTED = 'rej', _('Rejected')
        IN_PROGRESS = 'prg', _('In progress')

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.IN_PROGRESS)

    def get_status(self) -> Status:
        return self.Status(self.status)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student_idnp', 'internship_id'],
                name='unique_student_internship'
            )
        ]
        db_table = 'applications'