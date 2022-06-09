from distutils.command.upload import upload
from operator import mod
from django.db import models

# Create your models here.
class alarm(models.Model):
    pkey = models.IntegerField(primary_key=True)
    atime = models.CharField(max_length=5)

class toggle(models.Model):
    pkey = models.IntegerField(primary_key=True)
    intrudersys = models.BooleanField(default=False)
    led = models.BooleanField(default=False)
    stream = models.BooleanField(default=False)
    #pkey=1 IDS pkey=2 Led

class intruder(models.Model):
    category_id = models.AutoField(primary_key=True,null=False)
    intr_time = models.TextField(null=True)
    intr_date = models.TextField(null=True)
    picture = models.ImageField(upload_to ='pictures/',null = True)
    @property
    def picture_url(self):
        if self.picture :
            return self.picture.url

class intruder_stat(models.Model):
    pkey = models.IntegerField(primary_key=True,default=1)
    intr_state = models.BooleanField(default=False)

class owner(models.Model):
    name = models.TextField(max_length=100,primary_key=True,null=False)
    own_picture = models.ImageField(upload_to ='pictures/',null = True)