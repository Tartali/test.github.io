from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('avatar/', include('avatar.urls')),
    path('', include('registration.urls')),
    path('comments/', include('django_comments_xtd.urls')),
    path(r'jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('payments/', include('payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

