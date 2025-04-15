from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.companies.models import Company


class Internship(models.Model):
    class Stack(models.TextChoices):
        PYTHON = 'python', _('Python')
        JAVA = 'java', _('Java')
        DOT_NET = 'dot_net', _('.NET')
        REACT = 'react', _('React')
        GO_LANG = 'go_lang', _('Go Lang')
        CPP = 'cpp', _('C++')
        NEXT_JS = 'next_js', _('Next Js')
        NODE_JS = 'node_js', _('Node Js')
        JS_TS = 'js_ts', _('Javascript/Typescript')

    name = models.CharField(null=False)
    stack = models.CharField(null=False, choices=Stack.choices, default=Stack.PYTHON)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)

    def get_stack(self) -> Stack:
        return self.Stack(self.stack)

    class Meta:
        db_table = 'internships'