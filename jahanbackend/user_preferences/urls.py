from django.urls import path
from . import views

urlpatterns = [
    # Add your URL patterns here
    path('account/settings/', views.account_settings, name='account_settings'),
    path('account/update/', views.update_account_settings, name='update_account_settings'),
]

