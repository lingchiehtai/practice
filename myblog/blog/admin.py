from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post # 匯入 Post 模型
from ckeditor.widgets import CKEditorWidget
from django import forms

#admin.site.register(Post) # 註冊 Post 到後台

#CKEditor
class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

admin.site.register(Post, PostAdmin)

