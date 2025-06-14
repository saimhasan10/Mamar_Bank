# transactions/utils.py

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_transaction_email(user, amount, transaction_type, subject, template):
    message = render_to_string(
        template,
        {
            "user": user,
            "amount": amount,
            "transaction_type": transaction_type,
        },
    )
    email = EmailMultiAlternatives(subject, "", to=[user.email])
    email.attach_alternative(message, "text/html")
    email.send()
