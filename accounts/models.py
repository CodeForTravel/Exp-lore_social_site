from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
User = settings.AUTH_USER_MODEL


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email,password=None):

        if not username:
            raise ValueError('User must have an username! ')

        if not email:
            raise ValueError('User must have a email address! ')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)

        user.set_password(password)
        user.save(using = self._db)

        return user
    def create_superuser(self, username,email, password):
        user = self.create_user(username=username, email=email, password=password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using = self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    join_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name,self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    GenderChoice =(
        ('male', 'Male'),
        ('female','Female'),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    about_me = models.CharField(max_length=200,null=True, blank=True)
    current_city = models.CharField(max_length=200,null=True,blank=True)
    phone = models.CharField(max_length=20,null=True,blank=True)
    gender = models.CharField(max_length=10,choices = GenderChoice)
    bio = models.TextField(max_length=400,null=True,blank=True)
    birth_date = models.DateField(null=True,blank=True)
    image = models.ImageField(upload_to='images/',blank=True,null=True)

    def __str__(self):
        return self.user.username

def create_profile(sender , **kwargs):

	if kwargs['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender = User)
