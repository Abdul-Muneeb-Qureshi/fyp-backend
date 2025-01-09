from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserDetailAPIView , CreatePaymentAPIView , RefreshTokenAPIView

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('user', UserDetailAPIView.as_view(), name='user-detail'),  
    path('create-payment', CreatePaymentAPIView.as_view(), name='create-payment'),
    path('refersh-token', RefreshTokenAPIView.as_view(), name='refersh-token'),


]

