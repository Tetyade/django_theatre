from django.urls import path
import booking.views as views

urlpatterns = [
    path('', views.performance_list, name='performance_list'),
    path('<int:performance_id>/', views.performance_detail, name='performance_detail'),
    path('session/<int:session_id>', views.session_detail, name='session_detail'),
]