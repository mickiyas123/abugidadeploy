from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from discussions.models import Questions, Room ,Topic, Answers
from django.db.models import Q
import uuid


def generateUUID():
    return str(uuid4())



# Create your views here.

def home(request):
    return render(request, 'users/home.html')

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')
       

    return render(request, 'users/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')
def signupPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit =False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')



    context = {'form':form}  
    return render(request, 'users/signup.html',context)



# def profile(request, pk):
#     """ A function for retreving profile """
#     profile = Profile.objects.get(id=pk)
#     context ={'profile': profile}
#     return render(request, 'users/profile.html', context)


def profile(request, pk):
    """ A function for retreving profile """
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    

    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    profile = Profile.objects.get(id=pk)
    questions = Questions.objects.all()
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_discription = Room.description
    room_messages = Questions.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]
    context = {'profile': profile, 'questions': questions, 'rooms': rooms, 'topics': topics,'room_count': room_count, 'room_messages': room_messages, 'room_discription': room_discription}
    
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    """ A function for editing profile """
    profile = request.user.profile

    rooms = profile.room_set.all()
    context = {'profile': profile, 'rooms': rooms}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()

            return redirect('account')
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


def coursesPage(request):
    return render(request, 'users/course.html')
    
def aboutPage(request):
    return render(request, 'users/about.html')

