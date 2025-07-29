# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 17:05:58 2025

@author: user
"""

from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    title = models.CharField(max_length=200)
    #content = models.TextField()
    #content = RichTextField()
    content = RichTextUploadingField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # 新增圖片欄位
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時自動設定
    updated_at = models.DateTimeField(auto_now=True)      # 每次存檔都更新

    def __str__(self):
        return self.title

