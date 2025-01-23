from django.urls import include, path

from . import views


app_name = 'account'

urlpatterns = [
    path('', views.RegistrationView.as_view(), name='registration'),
]
