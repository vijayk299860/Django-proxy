# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from main_sheduler.models import EmailCredential, ScheduledEmail
from .serializers import EmailCredentialSerializer, ScheduledEmailSerializer
from main_sheduler.tasks import send_scheduled_email
from django.utils import timezone

class EmailCredentialViewSet(viewsets.ModelViewSet):
    queryset = EmailCredential.objects.all()
    serializer_class = EmailCredentialSerializer

    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        credential = self.get_object()
        try:
            # Test SMTP connection with credential
            password = credential.get_password()
            # Implement connection test logic here
            return Response({"status": "success", "message": "Connection successful"})
        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ScheduledEmailViewSet(viewsets.ModelViewSet):
    queryset = ScheduledEmail.objects.all()
    serializer_class = ScheduledEmailSerializer

    def perform_create(self, serializer):
        email = serializer.save()
        # Schedule the email task
        send_scheduled_email.apply_async(
            args=[email.id],
            eta=email.scheduled_time
        )
