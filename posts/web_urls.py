from django.urls import path
from .views_web import post_list, post_detail, post_create, post_edit

urlpatterns = [
    path('', post_list, name='web-post-list'),
    path('add/', post_create, name='web-post-add'),
    path('<int:pk>/', post_detail, name='web-post-detail'),
    path('<int:pk>/edit/', post_edit, name='web-post-edit'),
]
