from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login  # Renamed login to avoid conflict
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Room

@login_required(login_url='login')  # Added login_url argument to redirect to login page if not authenticated
def index(request):
    users = User.objects.all().exclude(username=request.user.username)
    return render(request, "chat/index.html", {"users": users})

@login_required(login_url='login')  # Added login_url argument to redirect to login page if not authenticated
def room(request, room_name):
    users = User.objects.all().exclude(username=request.user.username)
    room = Room.objects.get(id=room_name)
    return render(request, "chat/room_v2.html", {"room_name": room_name, "room": room, "users": users})

@login_required(login_url='login')  # Added login_url argument to redirect to login page if not authenticated
def start_chat(request, username):
    second_user = User.objects.get(username=username)
    try:
        room = Room.objects.get(first_user=request.user, second_user=second_user)
       
    except Room.DoesNotExist:
        try:
            room = Room.objects.get(second_user=request.user, first_user=second_user)
        except:

           room = Room.objects.create(first_user=request.user, second_user=second_user)
    return redirect("room", room.id)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Used the renamed login function
            return redirect('index')  # Replace 'index' with your desired redirect URL after login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'chat/login.html')
