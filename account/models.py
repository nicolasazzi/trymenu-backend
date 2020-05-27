import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManager(BaseUserManager):
    
    def create_user(self, email, username, first_name, last_name, password=None):
        user = self.model(
            email = self.normalize_email(email), 
            username = username, 
            first_name = first_name, 
            last_name = last_name
        )

        user.set_password(password)

        user.save(using=self._db)
        return user


    def create_superuser(self, email, username, first_name, last_name, password):

        user = self.create_user(
            email = self.normalize_email(email), 
            password = password,
            username = username, 
            first_name = first_name, 
            last_name = last_name
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)

    date_created = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True