# coding:utf-8
"""
    user's profile
"""
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

#from django.db.models.signals import post_save
#from django.dispatch import receiver


# Create your models here.


class Profile(models.Model):
    """
    用户注册信息及激活后的附加设置信息.
    """
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE
        )
    # 组织信息
    org_name = models.CharField('组织名称', max_length=100, blank=True)
    org_address = models.CharField('组织地址', max_length=200, blank=True)
    contract = models.CharField('联系人', max_length=32, blank=True)
    phone_number = models.CharField('注册手机号', max_length=32, blank=True)
    # aws 相关
    # aws options: accesskey,secret and region packet in token payload
    # external_id, arn, bucket, prefix and queue_size in response
    # if external_id and  arn is null, replace with user__name and bucket.
    access_key_id = models.CharField(max_length=64, blank=True)
    secret_access_key = models.CharField(max_length=64, blank=True)
    region = models.CharField(max_length=32, default='cn-north-1')
    external_id = models.CharField(max_length=64, blank=True)
    role_arn = models.CharField(max_length=64, blank=True)
    bucket = models.CharField(max_length=32, blank=True)
    # prefix of key end by '/'
    base = models.CharField('base', max_length=16, blank=True)
    # JSON example: "{'queueSize': 10,'partSize': 1000576"}
    options = models.CharField(max_length=128, blank=True)

    def __unicode__(self):
        return self.user.username

    
#@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

#@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
        instance.profile.save()
