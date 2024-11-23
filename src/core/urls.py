from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from main.views import NotFoundView

urlpatterns = [
    path(f'{settings.ADMIN_PATH}/login/', NotFoundView.as_view()),
    path(f'{settings.ADMIN_PATH}/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('', include('users.urls', namespace='user')),
    path('', include('booking.urls', namespace='booking')),
]

if settings.DEBUG:
    if settings.DEBUG_TOOLBAR:
        urlpatterns += [path('__debug__/', include('debug_toolbar.urls')),]
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
