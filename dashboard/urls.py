from django.urls import path
from . import views


app_name = 'dashboard'
urlpatterns = [
    path('', views.AlarmListView.as_view(), name='index'),
    path('<int:id>/', views.alarm_detail, name='alarm_detail'),
    path('<int:id>/share/', views.alarm_share, name='alarm_share'),
    path('<int:alarm_id>/comment/', views.alarm_comment, name='alarm_comment'),
]