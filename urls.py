"""
URL configuration for waste_management project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Customize admin site
admin.site.site_header = "Waste Management Administration"
admin.site.site_title = "Waste Management Admin"
admin.site.index_title = "Welcome to Waste Management Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contoler.urls')),
    path('api/', include('contoler.api_urls')),
    # Suppress Chrome DevTools 404
    path('.well-known/appspecific/com.chrome.devtools.json', RedirectView.as_view(url='/', permanent=False)),
]

# Serve static files in development
if settings.DEBUG:
    # Use staticfiles_urlpatterns for automatic static file serving
    urlpatterns += staticfiles_urlpatterns()
    # Also explicitly serve from STATICFILES_DIRS as fallback
    for static_dir in settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=static_dir)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Handler for 404 and 500 errors
handler404 = 'contoler.views.handler404'
handler500 = 'contoler.views.handler500'
