from django.urls import path
from . import views


urlpatterns = [

    path(
        'apply/<int:id>/',
        views.apply_job,
        name='apply_job'
    ),

    path(
        'my-applications/',
        views.my_applications,
        name='my_applications'
    ),

    path(
        'company-applicants/<int:id>/',
        views.company_applicants,
        name='company_applicants'
    ),

    path(
        'update-status/<int:id>/',
        views.update_status,
        name='update_status'
    ),

    path(
        'api/',
        views.application_api,
        name='application_api'
    ),
]