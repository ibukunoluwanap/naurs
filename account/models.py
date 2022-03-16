from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a admin with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = False
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    objects = UserManager()
    avatar = models.FileField("avatar", upload_to="avatar/", max_length=100, blank=True, null=True)
    first_name = models.CharField("first name", max_length=100, blank=False, null=False)
    last_name = models.CharField("last name", max_length=100, blank=False, null=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True) # is account activate
    staff = models.BooleanField(default=False) # a staff user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    date_joined = models.DateTimeField(default=timezone.now)

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their full name
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        # The user is identified by their short name
        return self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
