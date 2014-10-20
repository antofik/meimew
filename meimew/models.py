# coding=utf-8
import os
from django.db import models
import datetime


def get_upload_path(instance, filename):
    return os.path.join("user-files", instance.username, datetime.date.today().isoformat(), filename)


class File(models.Model):
    filename = models.CharField(max_length=256)
    slug = models.CharField(max_length=8)
    description = models.CharField(max_length=256, blank=True)
    username = models.CharField(max_length=64)
    data = models.FileField(upload_to=get_upload_path)
    path = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    size = models.IntegerField(default=0)
    downloaded_count = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super(File, self).__init__(*args, **kwargs)
        self.path = get_upload_path(self, '')

    def __unicode__(self):
        return '%s: %s' % (self.slug, self.name)
        
    class Meta: 
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        db_table = 'files'


class Entry(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    data = models.TextField()
    revision = models.FloatField()
    owner_id = models.CharField(max_length=64)
    family_id = models.CharField(max_length=128)

    class Meta:
        db_table = 'entries'
