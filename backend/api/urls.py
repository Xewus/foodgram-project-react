from django.urls import include, path
from . import views

app_name = 'api'

urlpatterns = [
    path('auth/', include('users.urls', namespace='users')),
]