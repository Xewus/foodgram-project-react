from django.contrib import admin
from django.urls import include, path

urlpatterns = (
    path('api/admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
)
