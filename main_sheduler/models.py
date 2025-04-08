from django.db import models
from django.conf import settings
from main_sheduler.utils import AESCipher
import base64


class EmailCredential(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    encrypted_password = models.BinaryField()
    iv = models.BinaryField()  # Initialization Vector storage
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def set_password(self, plain_password):
        cipher = AESCipher(settings.ENCRYPTION_KEY)
        encrypted = cipher.encrypt(plain_password)
        decoded = base64.b64decode(encrypted)
        self.iv = decoded[:AESCipher.bs]
        self.encrypted_password = decoded[AESCipher.bs:]

    def get_password(self):
        cipher = AESCipher(settings.ENCRYPTION_KEY)
        reconstructed = base64.b64encode(self.iv + self.encrypted_password)
        return cipher.decrypt(reconstructed)
    
    
class ScheduledEmail(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    
    credential = models.ForeignKey(EmailCredential, on_delete=models.CASCADE)
    recipients = models.TextField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    attachment = models.FileField(upload_to='email_attachments/', blank=True)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)