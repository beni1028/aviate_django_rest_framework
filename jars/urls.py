from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg import openapi 
from drf_yasg.views import get_schema_view as swagger_get_schem_view

schema_view = swagger_get_schem_view(
    openapi.Info(
        title = "All APIs",
        default_version = '3.0.0',
        description = "API Documentation",
    )

)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path("auth/", include("djoser.urls")),
    # path("auth/", include("djoser.urls.jwt")),
    path('api/applicant/',include("api.urls")),
    path('swagger/schema/',schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/schema/', schema_view.with_ui('redoc', cache_timeout=0))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)