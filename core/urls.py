from django.contrib import admin
from django.urls import path, include
from .views import index
from django.contrib.auth import views as auth_views
from users.forms import (
    BootstrapAuthenticationForm,
    BootstrapPasswordResetForm,
)
from django.conf import settings
from django.conf.urls.static import static
from posts.views import post_create

from users.views_web import register

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/posts/', include('posts.urls')),

    # Simple web UI for posts
    path('posts/', include('posts.web_urls')),

    path('create/', post_create, name='create_post'),
    # include Django's built-in auth views but override login and password reset with bootstrap forms
    path('accounts/login/', auth_views.LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=BootstrapAuthenticationForm,
        ),
        name='login',
    ),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            form_class=BootstrapPasswordResetForm,
        ),
        name='password_reset',
    ),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done',
    ),
    path('accounts/register/', register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
