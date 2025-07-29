from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'), # 文章列表
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # 詳細頁
    path('post/new/', views.post_new, name='post_new'),  # 新增這行
]
