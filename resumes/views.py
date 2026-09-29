from django.shortcuts import render, redirect

from .models import Resume
from .utils import extract_text_from_pdf, extract_skills
from accounts.models import Profile

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import ResumeSerializer


def upload_resume(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != 'candidate':

        return redirect('home')

    if request.method == 'POST':

        resume_file = request.FILES['resume']

        resume = Resume.objects.update_or_create(
            candidate=request.user,
            defaults={
                'resume_file': resume_file
            }
        )[0]

        text = extract_text_from_pdf(
            resume.resume_file.path
        )

        skills = extract_skills(text)

        resume.extracted_text = text
        resume.skills = ', '.join(skills)

        resume.save()

        return render(
            request,
            'resume_upload.html',
            {
                'uploaded': True,
                'skills': skills
            }
        )

    return render(
        request,
        'resume_upload.html'
    )


@api_view(['GET'])
def resume_api(request):

    if not request.user.is_authenticated:

        return Response(
            {'error': 'Login required'},
            status=401
        )

    resumes = Resume.objects.filter(
        candidate=request.user
    )

    serializer = ResumeSerializer(
        resumes,
        many=True
    )

    return Response(serializer.data)