from __future__ import unicode_literals

# Create your models here.
from django.db import models
import hashlib
from projectmanage.models import Projects

class User(models.Model):
    username =  models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    login_time = models.DateTimeField(auto_now_add=True)
    login_ip = models.GenericIPAddressField()
    group = models.ManyToManyField(Group)  

    def is_authenticated(self):
        return True

    def hashed_password(self, password=None):
        if not password:
            return self.password
        else:
            return hashlib.md5(password).hexdigest()
          
    def check_password(self, password):
        if self.hashed_password(password) == self.password:
            return True
        return False

    class Meta:
        db_table = "k8s_users"

class Group(models.Model):
    groupname =  models.CharField(max_length=12, unique=True)
    comment = models.CharField(max_length=24, blank=True, null=True)

    class Meta:
        db_table = "k8s_groups"

class GroupPermission(models.Model):
    groupid = models.ForeignKey(GROUPS, on_delete=models.CASCADE)
    projectid = models.ForeignKey(Projects, on_delete=models.CASCADE)

    class Meta:
        db_table = "k8s_groups_permission"
        unique_together = ('groupid', 'projectid')

