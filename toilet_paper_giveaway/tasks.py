from celery import shared_task
from django.core.mail import send_mail


@shared_task()
def send_email_w_celery(name: str, last_name: str, email: str):
    """
    Using django send_email method, to send a simple email for a new
    participant.

    :param name: Participant Name
    :type name: str
    :param last_name: Participant Lastname
    :type last_name: str
    :param email: Participant email
    :type email: str
    :return: Email Sent Message
    :rtype: str
    """
    send_mail(
        "Welcome to Toilet Paper Giveaway",
        "",
        "gjmm1711@gmail.com",
        [email],
        html_message=f"Thank you {name} {last_name} for participate, "
        f"please click  <a href='{email}'>Here</a> to create password ",
    )
    return "Email sent"
