from celery import shared_task
from mail_templated import EmailMessage

@shared_task
def SendEmailWithCelery(template:str, token:str, sender:str, receiver:list):
    message = EmailMessage(
                template,
                {"token": token},
                sender,
                to=receiver,
            )
    message.send()