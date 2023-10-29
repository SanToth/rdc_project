from django.urls import path
from django.contrib.auth import views as auth_views
from . import forms
from django.urls import reverse_lazy

app_name = 'account'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='account/login.html', 
        authentication_form=forms.CustomLoginForm), 
        name='login' ),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='account/logout.html', 
        next_page='account:logout'), 
        name='logout'),

    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='account/password_change.html', 
        form_class=forms.CustomPasswordChangeForm,
        success_url='/account/password-change/done/'
        ), 
        name='password_change'),

    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='account/password_change_done.html',), 
         name='password_change_done'),
]