
from django.db import models
from django.contrib.auth.models import User

class UserPlus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    chinese_name = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return self.user.username
