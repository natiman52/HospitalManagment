from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import datetime
from patient.models import Hospital
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

types = [
    ('Doctor' ,'Doctor'),
    ('Admin',"Admin"),
    ("Nurse","Nurse")
]
specialist=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_("you need a username"))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, password, **extra_fields)
# Create your models here.
def uploadTo(instance,filename):
    username = instance.username
    return f'upload/{username}/{filename}'
def defaultCreate(instance,*args,**kwargs):
    if instance.sex == 'male':
        return 'defaults/male.jpg'
    else:
        return 'defaults/female.jpg'
class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=95,unique=True)
    firstname=models.CharField(max_length=75)
    lastname=models.CharField(max_length=75)
    grandname =models.CharField(max_length=75,blank=True,null=True)
    sex =models.CharField(choices=[('male',"male"),('female',"female")],max_length=50)
    pic =models.ImageField(upload_to=uploadTo,default='defaults/male.jpg')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=datetime.date.today)
    type =models.CharField(choices=types,default='Nurse',max_length=55) 
    email =models.EmailField(default='default@gmail.com')
    phone =PhoneNumberField(default='+2519876453')
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['lastname','firstname']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

class Doctor(models.Model):
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE,default=1,related_name='profile')
    hospital =models.ForeignKey(Hospital,on_delete=models.SET_NULL,blank=True,null=True)
    speciality = models.CharField(max_length=150,choices=specialist,default=1)
    Adreess = models.CharField(max_length=200,default='Addis Abeba,boyle adebabay geba below')
class Nurse(models.Model):
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE,default=1,related_name='profile2')
    hospital =models.ForeignKey(Hospital,on_delete=models.CASCADE)
    Adreess = models.CharField(max_length=200,default='Addis Abeba,boyle adebabay geba below')
class Verification(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    type = models.CharField(choices=types,default='Nurse',max_length=55)
    active = models.BooleanField(default=True)

@receiver(pre_save, sender=MyUser)
def check_beard(sender, instance=None, created=False, **kwargs):
    if(not instance.pic):
        if instance.sex == 'male': # Check instance id if it saving for first time, and set default
            instance.pic ='defaults/male.jpg'
        else :
            instance.pic ='defaults/female.jpg'
@receiver(post_save,sender=MyUser)
def create_verfiy(sender,instance,created,**kwargs):
    if(created):
        verObj = Verification(user=instance,type=instance.type)
        verObj.save()