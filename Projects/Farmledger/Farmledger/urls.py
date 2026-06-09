"""
URL configuration for Farmledger project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
try:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
    SPECTACULAR_AVAILABLE = True
except Exception:
    SPECTACULAR_AVAILABLE = False

urlpatterns = [
    path('admin/', admin.site.urls),
    # Conditional OpenAPI docs (drf-spectacular optional)
    *( [path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')] if SPECTACULAR_AVAILABLE else [] ),
    path('api/v1/weather/', include('apps.weather.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/', include('apps.accounts.urls')),
    path('api/v1/', include('apps.farms.urls')),
    path('api/v1/', include('apps.crops.urls')),
    path('api/v1/', include('apps.expenses.urls')),
    path('api/v1/', include('apps.harvests.urls')),
]
