from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('ip/', views.IP_APIView.as_view(), name='ip_address'),
    path('datetime/', views.ServerDateTimeAPIView.as_view(), name='datetime'),
    path('client-datetime/', views.DateTimeAPIView.as_view(), name='client_datetime'),
    path('datetime/seconds/', views.DateTimeSecondsAPIView.as_view(), name='seconds'),
    path('user-list/', views.UserListAPIView.as_view(), name='user_list'),
    path('users/', views.UserListAPIView.as_view(), name='users'),

    # HTMX
    path('generate-key/', views.GenerateKeyAPIView.as_view(), name='generate_key'),
    path('test/', views.TestHtmxAPIView.as_view(), name='htmx_test'),
    path('htmx-modal/', views.ModalWindowAPIView.as_view(), name='htmx_modal'),
    path('users/check_username/', views.CheckUsernameAPIView.as_view(),
         name='check_username'),
    path('users/check_email/', views.CheckEmailAPIView.as_view(), name='check_email'),
    path('tabs/<str:text>/', views.HtmxTabsAPIView.as_view(),
         name='htmx_tabs'),
]
