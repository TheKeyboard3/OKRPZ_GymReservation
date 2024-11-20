from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register-wait/', views.ResetWaitView.as_view(), 
         name='reset_wait'),
    path('confirm/<token>/', views.RegisterConfirmView.as_view(),
         name='register_confirm'),
    path('reset-request/', views.PasswordResetView.as_view(),
         name='password_reset'),
    path('reset-confirm/<token>/', views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('client-change/', views.ProfileChangeView.as_view(), 
         name='client_profile_change'),
    path('trainer-change/', views.ProfileChangeView.as_view(), 
         name='trainer_profile_change'),
    path('profile/<int:id>/', views.ProfileDetailView.as_view(), 
         name='detail')
]
