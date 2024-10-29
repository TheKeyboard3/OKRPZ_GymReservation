from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about', views.AboutView.as_view(), name='about'),
    path('host', views.HostInfoView.as_view(), name='host'),
    path('htmx-examples', views.HTMXExamplesView.as_view(), name='htmx_examples'),
    path('test-func', views.HTMXExamplesView.as_view(), name='test_func'),
    path('send-email', views.SendEmailView.as_view(), name='test_email'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
