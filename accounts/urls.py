
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [

    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('profile_create/',views.ProfileCreateView.as_view(),name = 'profile_create'),
    path('edit_profile/',views.EditProfileView.as_view(),name = 'edit_profile'),

#password change
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change-complete/', views.PasswordChangeCompleteView.as_view(), name= 'passwoerd_change_complete'),



#password Reset
    path('password-reset/', views.PasswordResetView.as_view(),name='password_reset'),

    path('password-reset/done/', views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
#password Reset complete



]