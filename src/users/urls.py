from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
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
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/', views.ProfileDetailView.as_view(),
         name='detail')
]
