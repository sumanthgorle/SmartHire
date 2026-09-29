from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:id>/', views.job_detail, name='job_detail'),
    path('create/', views.create_job, name='create_job'),
    path('company-dashboard/', views.company_dashboard, name='company_dashboard'),
    path('api/', views.job_api, name='job_api'),
]