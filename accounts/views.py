from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import Profile

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import RegisterSerializer, LoginSerializer


def home(request):

    if request.user.is_authenticated:

        profile = Profile.objects.get(
            user=request.user
        )

        return render(
            request,
            'home.html',
            {'profile': profile}
        )

    return render(
        request,
        'home.html'
    )


def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST['phone']
        bio = request.POST['bio']
        role = request.POST['role']

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Profile.objects.create(
            user=user,
            role=role,
            phone=phone,
            bio=bio
        )

        return redirect('home')

    return render(
        request,
        'register.html'
    )


def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect('home')

        else:

            return render(
                request,
                'login.html',
                {
                    'error': 'Invalid username or password'
                }
            )

    return render(
        request,
        'login.html'
    )


def logout_view(request):

    logout(request)

    return redirect('home')


def candidate_dashboard(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if profile.role != 'candidate':

        return redirect('home')

    return render(
        request,
        'candidate_dashboard.html',
        {'profile': profile}
    )


@api_view(['POST'])
def register_api(request):

    serializer = RegisterSerializer(
        data=request.data
    )

    if serializer.is_valid():

        user = serializer.save()

        profile = Profile.objects.get(
            user=user
        )

        return Response({
            'message': 'User registered successfully',
            'username': user.username,
            'role': profile.role
        })

    return Response(
        serializer.errors,
        status=400
    )


@api_view(['POST'])
def login_api(request):

    serializer = LoginSerializer(
        data=request.data
    )

    if serializer.is_valid():

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:

            profile = Profile.objects.get(
                user=user
            )

            return Response({
                'message': 'Login successful',
                'username': user.username,
                'role': profile.role
            })

        return Response(
            {
                'message': 'Invalid username or password'
            },
            status=401
        )

    return Response(
        serializer.errors,
        status=400
    )