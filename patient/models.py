from typing import Any
from django.db import models
import datetime
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
level =[("Primary",'Primary'),("Secondary",'Secondary'),("Tertiary","Tertiary")]
types = [
    ('Geriatric hospitals',"Geriatric hospitals"),
    ('Psychiatric hospitals','Psychiatric hospitals'),
    ('Clinics','Clinics'),
    ('Specialty Hospitals','Specialty Hospitals'),
    ('Ophthalmology','Ophthalmology'),
    ('Dental Hospital','Dental Hospital'),
    ('Anesthesiologists','Anesthesiologists')
]
disease_types = [
    ('infectious diseases',"infectious diseases"),
    ('deficiency diseases',"deficiency diseases"),
    ('hereditary diseases',"hereditary diseases"),
    ('physiological diseases',"physiological diseases"),
    ('Allergies','Allergies'),
    ('Colds and Flu',"Colds and Flu"),
    ('Conjunctivitis','Conjunctivitis'),
    ('Headaches','Headaches'),
    ('Stomach Aches','Stomach Aches'),
    ("Broken Bones","Broken Bones")
]
blood =[
    ('A+',"A+"),
    ('A-',"A-"),
    ('B+',"B+"),
    ('B-',"B-"),
    ('O+',"O+"),
    ('O-',"O-"),
    ('AB+',"AB+"),
    ('AB-',"AB-"),
]
class Hospital(models.Model):
    name=models.CharField(max_length=80)
    location =models.CharField(max_length=200)
    level = models.CharField(max_length=50,choices=level)
    speciality = models.CharField(max_length=150,choices=types)
    img =models.ImageField(upload_to='hospitals/',default='defaults/logo.webp')

    def __str__(self, *args, **kwargs):
        return self.name

def patientUpload(instance,filename):
    return f"patient/{instance.id}/{filename}"

class Patient(models.Model):
    id = models.CharField(max_length=12,unique=True,primary_key=True)
    firstname =models.CharField(max_length=30)
    lastname =models.CharField(max_length=30)
    grandname =models.CharField(max_length=75,blank=True,null=True)
    sex = models.CharField(choices=[('male',"male"),('female','female')],max_length=150)
    pic = models.ImageField(upload_to=patientUpload)
    age = models.IntegerField(default=18)
    date_of_birth =models.DateField(default='1997-07-01')
    phone =PhoneNumberField(blank=True,null=True)
    gmail =models.EmailField(blank=True,null=True)
    blood =models.CharField(choices=blood,max_length=12,default='A+')
    def __str__(self,*args,**kwargs):
        return f"{self.firstname} {self.lastname}"

class PatientRecord(models.Model):
    patient =models.ForeignKey(Patient,on_delete=models.CASCADE)
    date =models.DateField(default=datetime.date.today)
    hospital =models.ForeignKey(Hospital,on_delete=models.SET_NULL,null=True,blank=True)
    reason =models.TextField()
    Recommandation = models.TextField(null=True,blank=True)
    type = models.CharField(choices=disease_types,max_length=200,default="Stomach Aches")
