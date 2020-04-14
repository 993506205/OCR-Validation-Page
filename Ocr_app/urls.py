from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('pages.urls')),
    path('ocrfiles/', include('ocrfiles.urls')),
    path('accounts/', include('accounts.urls')),
    # path('validations/', include('validations.urls')),
    path('dirprojects/', include('dirprojects.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
