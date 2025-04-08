# serializers.py
from rest_framework import serializers
from main_sheduler.models import EmailCredential, ScheduledEmail

class EmailCredentialSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = EmailCredential
        fields = ['id', 'name', 'email', 'password']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        credential = EmailCredential(**validated_data)
        credential.set_password(password)
        credential.save()
        return credential
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class ScheduledEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledEmail
        fields = '__all__'
        read_only_fields = ['status', 'sent_at']
