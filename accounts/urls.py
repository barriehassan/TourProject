from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, CustomLogoutView, RegisterTouristView
from .forms import CustomSetPasswordForm, CustomPasswordResetForm

app_name = "accounts"


urlpatterns = [
    path('register/', RegisterTouristView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')),
         name='reset_password'),
    path('reset_password_done/',
         auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('accounts:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
