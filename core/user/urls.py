from django.urls import path

from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    # Auth
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', views.UserCreateView.as_view()),
    
    # Refer
    path('refer/', views.ReferCreateView.as_view()),
    path('refer_delete/<int:pk>/', views.ReferDeleteView.as_view()),
    path('user_detail/<int:pk>/', views.UserDetailView.as_view()),
    path('refer_receive/', views.EmailView.as_view())
]
