from django.db import models


class Company(models.Model):
    name = models.CharField(null=False, unique=True)
    web_url = models.CharField(default=None, blank=True, null=True)
    email = models.EmailField(null=True, unique=True, default=None)

    class Meta:
        db_table = 'companies'

    def __str__(self):
        return self.name