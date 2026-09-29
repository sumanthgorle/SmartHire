from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Job
from accounts.models import Profile
from applications.models import Application

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import JobSerializer


def job_list(request):

    jobs = Job.objects.all()

    return render(
        request,
        'job_list.html',
        {'jobs': jobs}
    )


def job_detail(request, id):

    job = Job.objects.get(id=id)

    match_percentage = None
    ai_match_percentage = None
    final_match_percentage = None

    matched_skills = []
    missing_skills = []

    recommendation = ""

    profile = None
    already_applied = False

    if request.user.is_authenticated:

        try:

            profile = Profile.objects.get(
                user=request.user
            )

        except Profile.DoesNotExist:

            profile = None

        try:

            resume = request.user.resume

            from resumes.utils import (
                match_skills,
                calculate_ai_match
            )

            (
                matched_skills,
                missing_skills,
                match_percentage,
                recommendation
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

            ai_match_percentage = calculate_ai_match(
                resume.extracted_text,
                job_text
            )

            final_match_percentage = (
                (match_percentage * 0.70)
                + (ai_match_percentage * 0.30)
            )

            final_match_percentage = round(
                final_match_percentage,
                2
            )

        except Exception as e:

            print(
                "RESUME MATCH ERROR:",
                e
            )

        if profile and profile.role == 'candidate':

            already_applied = Application.objects.filter(
                candidate=request.user,
                job=job
            ).exists()

    return render(
        request,
        'job_detail.html',
        {
            'job': job,
            'profile': profile,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'match_percentage': match_percentage,
            'ai_match_percentage': ai_match_percentage,
            'final_match_percentage': final_match_percentage,
            'recommendation': recommendation,
            'already_applied': already_applied
        }
    )


@login_required(login_url='login')
def create_job(request):

    try:

        profile = Profile.objects.get(
            user=request.user
        )

    except Profile.DoesNotExist:

        return redirect('home')

    if profile.role != 'company':

        return redirect('job_list')

    if request.method == 'POST':

        title = request.POST['title']
        description = request.POST['description']
        required_skills = request.POST['required_skills']
        location = request.POST['location']
        salary = request.POST['salary']

        Job.objects.create(
            company=request.user,
            title=title,
            description=description,
            required_skills=required_skills,
            location=location,
            salary=salary
        )

        return redirect('job_list')

    return render(
        request,
        'create_job.html'
    )


@login_required(login_url='login')
def company_dashboard(request):

    try:

        profile = Profile.objects.get(
            user=request.user
        )

    except Profile.DoesNotExist:

        return redirect('home')

    if profile.role != 'company':

        return redirect('job_list')

    jobs = Job.objects.filter(
        company=request.user
    )

    for job in jobs:

        job.applicants = Application.objects.filter(
            job=job
        )

        job.applicant_count = job.applicants.count()

    return render(
        request,
        'company_dashboard.html',
        {
            'jobs': jobs
        }
    )


@api_view(['GET'])
def job_api(request):

    if not request.user.is_authenticated:

        return Response(
            {'error': 'Login required'},
            status=401
        )

    jobs = Job.objects.all()

    serializer = JobSerializer(
        jobs,
        many=True
    )

    return Response(
        serializer.data
    )