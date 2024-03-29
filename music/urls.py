from django.urls import path, re_path
from . import views

app_name = 'music'

urlpatterns = [
    path('',views.index, name="index"),
    re_path(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    path('register/',views.UserFormView.as_view(), name='register'),
    path('login/',views.login_user, name='login_user'),
]
