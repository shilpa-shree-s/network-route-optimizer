from django.urls import path
from .views import(
    RegisterView,
    LoginUser,
    LogoutView
)

urlpatterns=[
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', LoginUser.as_view(), name='login_user'),
    path('logout/', LogoutView.as_view(), name='logout')
]