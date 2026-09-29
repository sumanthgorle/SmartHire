from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Application
from jobs.models import Job
from accounts.models import Profile

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import ApplicationSerializer


@login_required
def apply_job(request, id):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != 'candidate':
        return redirect('job_list')

    job = Job.objects.get(id=id)

    if request.method == 'POST':

        application = Application.objects.filter(
            candidate=request.user,
            job=job
        ).first()

        if application is None:

            Application.objects.create(
                candidate=request.user,
                job=job
            )

        return redirect('my_applications')

    return redirect(
        'job_detail',
        id=job.id
    )


@login_required
def my_applications(request):

    applications = Application.objects.filter(
        candidate=request.user
    )

    return render(
        request,
        'my_applications.html',
        {'applications': applications}
    )


@login_required
def company_applicants(request, id):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != 'company':
        return redirect('job_list')

    job = Job.objects.get(id=id)

    if job.company != request.user:
        return redirect('job_list')

    applications = Application.objects.filter(
        job=job
    )

    from resumes.utils import (
        match_skills,
        calculate_ai_match
    )

    for application in applications:

        application.match_percentage = None
        application.ai_match_percentage = None
        application.final_match_percentage = None

        application.matched_skills = []
        application.missing_skills = []

        application.recommendation = ""

        try:

            resume = application.candidate.resume

            (
                application.matched_skills,
                application.missing_skills,
                application.match_percentage,
                application.recommendation
            ) = match_skills(
                resume.skills,
                job.required_skills
            )

            job_text = (
                job.title
                + " "
                + job.description
                + " "
                + job.required_skills
            )

            application.ai_match_percentage = calculate_ai_match(
                resume.extracted_text,
                job_text
            )

            application.final_match_percentage = (
                (application.match_percentage * 0.70)
                + (application.ai_match_percentage * 0.30)
            )

            application.final_match_percentage = round(
                application.final_match_percentage,
                2
            )

        except Exception as e:

            print(
                "APPLICANT MATCH ERROR:",
                e
            )

    return render(
        request,
        'company_applicants.html',
        {
            'applications': applications
        }
    )


@login_required
def update_status(request, id):

    application = Application.objects.get(
        id=id
    )

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != 'company':
        return redirect('job_list')

    if application.job.company != request.user:
        return redirect('job_list')

    if request.method == 'POST':

        status = request.POST.get('status')

        if status in [
            'applied',
            'shortlisted',
            'rejected',
            'interview',
            'selected'
        ]:

            application.status = status
            application.save()

    return redirect(
        'company_applicants',
        application.job.id
    )


@api_view(['GET'])
def application_api(request):

    if not request.user.is_authenticated:

        return Response(
            {'error': 'Login required'},
            status=401
        )

    applications = Application.objects.filter(
        candidate=request.user
    )

    serializer = ApplicationSerializer(
        applications,
        many=True
    )

    return Response(
        serializer.data
    )