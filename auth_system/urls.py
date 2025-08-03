from django.urls import path
from django.contrib.auth.views import LogoutView
from auth_system import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='performance_list'), name='logout'),
]