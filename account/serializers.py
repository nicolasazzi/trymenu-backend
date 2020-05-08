from rest_framework import serializers
from .models import Account

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class AccountRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['email', 'username', 'first_name', 'password', 'last_name']
        

    def save(self):

        account = Account(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name']
        )

        password = self.validated_data['password']

        account.set_password(password)
        account.save()

        return account


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)