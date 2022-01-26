from django.core.mail import EmailMessage
from django.conf import settings


def enviarEmail(subject, body, to, from_email = 'piurabonita@munipiura.gob.pe', bcc = None, attachments = None, contentHTML = True ):
    
    email = EmailMessage(
    subject,
    body,
    from_email,
    to,
    bcc,
    )

    if contentHTML:
        email.content_subtype = "html"

    if attachments:
        for attachment in attachments:
            email.attach_file(attachment)

    return email.send()

    



