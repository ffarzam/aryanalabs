from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('update/', views.UpdateProfile.as_view(), name='update'),
    path('login/refresh/', views.RefreshToken.as_view(), name='token_refresh'),
    path('profile/', views.ShowProfile.as_view(), name='profile'),

]
