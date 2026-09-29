from django.urls import path
from . import views


urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path(
        'candidate-dashboard/',
        views.candidate_dashboard,
        name='candidate_dashboard'
    ),

    path(
        'register/api/',
        views.register_api,
        name='register_api'
    ),

    path(
        'login/api/',
        views.login_api,
        name='login_api'
    ),
]