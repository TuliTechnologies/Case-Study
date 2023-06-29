
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.template.loader import render_to_string
from django.urls import reverse


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create a user email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    """
    email and password are required.
    """

    TYPE = (
        ('front_user', 'front_user'),
        ('supplier', 'supplier'),
        ('admin', 'admin'),
        ('studio', 'studio')
    )


    GENDER = (
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other')
    )

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    middle_name = models.CharField(_('middle name'), max_length=150, null=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True, null=False)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    type = models.CharField(max_length=10, choices=TYPE, default=TYPE[2][0])
    phone = models.CharField(max_length=15, default=None, null=True, blank=True)
    gender  = models.CharField(max_length=6, choices=GENDER, null=True)
    date_of_birth  = models.DateField(null=True, blank=True)
    address = models.CharField(_('address'), max_length=150, blank=True)
    town = models.CharField(_('town'), max_length=150, blank=True)
    invoice_email = models.CharField(_('invoice email'), max_length=150, blank=True)
    is_deleted=models.BooleanField(default=False)
    deleted_at=models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name



from django.core.mail import EmailMultiAlternatives

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    url = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    context = {
        'current_user': reset_password_token.user,
        'url': url

    }
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)
    email_html_message = render_to_string('email/user_reset_password.html', context)
    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for Digital Press",
        # message:
        email_plaintext_message,
        # from:
        "donotreply@digitalpress.co.uk",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()