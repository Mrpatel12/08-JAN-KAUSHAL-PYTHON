from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin-panel/', include('AdminApp.urls')),
    path('admin/', admin.site.urls),
    path('', include('UserApp.urls')),
]
