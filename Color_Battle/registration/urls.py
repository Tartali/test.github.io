from django.urls import path
from . import views
# from django.conf.urls import url
from .views import Profile, Comment2, YandexNotifications
from django.contrib import admin
admin.autodiscover()
poll_id = 1

urlpatterns = [
    path('profile/<str:username>/', Profile.as_view(), name='profile'),
    path('', views.home, name='home'),
    path('black', views.black, name='black'),
    path('white', views.white, name='white'),
    path('purple', views.purple, name='purple'),

    path('notifications/', YandexNotifications.as_view(), name='notifications'),
    path('callback/', views.callback_payment, name='callback'),
    path('info', Comment2.as_view(), name='comment'),

    # path('pay/<int:payment_id>/', views.payment_details, name='pay'),

    path('black_results', views.black_results, name='black_results'),
    path('white_results', views.white_results, name='white_results'),
]

