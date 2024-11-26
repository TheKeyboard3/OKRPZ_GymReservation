from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views


app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about', views.AboutView.as_view(), name='about'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
