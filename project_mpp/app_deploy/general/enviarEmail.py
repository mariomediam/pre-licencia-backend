from django.core.mail import EmailMessage
from django.conf import settings


def enviarEmail(subject, body, to, from_email = 'informatica@munipiura.gob.pe', bcc = None, attachments = None, contentHTML = True ):
    
    email = EmailMessage(
    subject = subject,
    body = body,
    from_email = from_email,
    to = to,
    bcc = bcc,
    )

    if contentHTML:
        email.content_subtype = "html"

    if attachments:
        for attachment in attachments:
            email.attach_file(attachment)

    return email.send()

    



