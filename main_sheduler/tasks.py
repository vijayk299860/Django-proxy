# tasks.py
from celery import shared_task
from django.core.mail import EmailMessage
from django.utils import timezone
import smtplib
from .models import ScheduledEmail

@shared_task
def send_scheduled_email(email_id):
    try:
        # Get the email to send
        email = ScheduledEmail.objects.get(id=email_id)
        
        # Skip if already sent
        if email.status == 'sent':
            return
        
        # Get credential and password
        credential = email.credential
        password = credential.get_password()
        
        # Create email message
        msg = EmailMessage(
            subject=email.subject,
            body=email.body,
            from_email=credential.email,
            to=email.recipients.split(','),
        )
        
        # Add attachment if any
        if email.attachment:
            msg.attach_file(email.attachment.path)
        
        # Configure SMTP connection
        msg.connection = smtplib.SMTP(
            host='smtp.gmail.com',  # This should be configurable
            port=587
        )
        msg.connection.starttls()
        msg.connection.login(credential.email, password)
        
        # Send email
        msg.send()
        
        # Update status
        email.status = 'sent'
        email.sent_at = timezone.now()
        email.save()
        
        return f"Email {email_id} sent successfully"
        
    except Exception as e:
        # Update status to failed
        if 'email' in locals():
            email.status = 'failed'
            email.save()
        
        # Re-raise for Celery to handle
        raise e
