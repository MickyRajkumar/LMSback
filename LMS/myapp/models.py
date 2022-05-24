from django.db import models
from setuptools import Require
from datetime import datetime, timedelta

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.timezone import now


class CustomAccountManager(BaseUserManager):

    def create_superuser(self,  email, user_name,  default_address, mobile, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, default_address, mobile, password, **other_fields)

    def create_user(self, email, user_name, default_address, mobile, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          default_address= default_address, mobile = mobile, password = password, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    default_address = models.CharField(max_length=100, null=True, default=None, blank=True)
    sem = models.IntegerField(null=True, default=None, blank=True)
    roll_no = models.IntegerField(blank=True, default=None, null=True)
    mobile = models.IntegerField(blank=True, null=True)
    user_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10, default=None, blank=True, null=True)
    course = models.CharField(max_length=100, default=None, blank=True, null=True)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name','default_address', 'mobile']

    def __str__(self):
        return self.user_name


        
class BookCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    

    def __str__(self):
        return self.name

class book(models.Model):
    book_name = models.CharField(max_length=50)
    author_name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to ='images/', default=None, blank=True)
    stock = models.IntegerField(default=1)
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.book_name

class borrow(models.Model):

    def get_deadline():
        return datetime.today() + timedelta(days=15)

    book = models.ForeignKey(book, default=None, db_column='book_name',on_delete=models.CASCADE)
    student = models.ForeignKey(NewUser, related_name="user", on_delete=models.CASCADE)
    mobile = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=50)
    issue_date = models.DateTimeField(default=now)
    due_date = models.DateTimeField(default = get_deadline())

    def __str__(self):
        return self.student.user_name

class comment(models.Model):
    comment = models.TextField()
    student = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    book = models.ForeignKey(book,on_delete=models.CASCADE)
    time = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:15] + ".... " + "by " + self.student.user_name