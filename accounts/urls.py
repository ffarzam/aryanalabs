from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('update/', views.UpdateProfile.as_view(), name='update'),
    path('login/refresh/', views.RefreshToken.as_view(), name='token_refresh'),
    path('profile/', views.ShowProfile.as_view(), name='profile'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('delete/', views.DeleteUser.as_view(), name='delete'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('logout_all/', views.LogoutAll.as_view(), name='logout_all'),
    path('active_login/', views.CheckAllActiveLogin.as_view(), name='active_login'),
    path('selected_logout/', views.SelectedLogout.as_view(), name='selected_logout'),
]
