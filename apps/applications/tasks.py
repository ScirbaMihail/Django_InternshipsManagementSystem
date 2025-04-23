from django.conf import settings
from django.core.mail import send_mail

from apps.applications.models import Application


def send_notification(company_name, company_mail, student_name, student_mail, internship_title, internship_status):
    # Company email message data
    company_subject = f'Internship result'
    company_message = f'Student {student_name} has been approved to {internship_title}!' \
        if internship_status == Application.Status.APPROVED \
        else f'Student {student_name} has been rejected to internship'

    # Student email message data
    student_subject = f'Company {company_name}'
    student_message = f'Congratulations, {student_name}. \n You have been approved to {internship_title}!' \
        if internship_status == Application.Status.APPROVED \
        else f'Apologies, {student_name}.\n You have been rejected to {internship_title}'

    # Send mail to company
    send_mail(
        subject=company_subject,
        message=company_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[company_mail],
        fail_silently=False,
    )

    # Send mail to student
    send_mail(
        subject=student_subject,
        message=student_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[student_mail],
        fail_silently=False,
    )

    # Print the result in logs
    print(f'[ GMAIL ] -> sent to {company_mail}, {student_mail}')