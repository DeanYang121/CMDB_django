from django.db import models
import django.utils.timezone as timezone
import hashlib
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    sign_date = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return '%d'%self.pk
    def save(self,*args,**kwargs):
        self.password = hashlib.sha1(self.password.encode("utf8")+self.username.encode("utf8")).hexdigest()
        super(User, self).save(*args,**kwargs)





