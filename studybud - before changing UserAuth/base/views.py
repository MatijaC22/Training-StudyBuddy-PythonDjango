# from tkinter import CASCADE
from django.shortcuts import render, redirect #redirect will redirect the user
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm


# Create your views here.
# rooms = [# dictionary
#     {'id':1, 'name':'Lets learn python!'},
#     {'id':2, 'name':'Desing with me'},
#     {'id':3, 'name':'Frontend developers'},
# ]

def loginPage(request):

    page = 'login'

    if request.user.is_authenticated: #if user is login he cant be on this login page
        return redirect('home')


    if request.method =='POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try: 
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context={'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    #page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form':form} )

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)

        )
    #rooms = Room.objects.all() #kada koristimo model manage uzmemo model (u nasem slucaju Room) zatim .objects i na kraju biramo methodu kojom zelimo manipulirati
    #model manager - nista nego upravljanje nasim modelsima i manipulirnanje datom
    
    topics =Topic.objects.all()[0:5]   #limitiranje da prikaze samo prvih 5 topics
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages': room_messages} #napravi dictionary key 'rooms' data rooms
    return render(request, 'base/home.html', context) # render uzima http request i template stranicu htmla
#zelimo dictionary rooms pozvati u nasem htmlu home


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all() #.order_by('-created') #u message ce biti upisane children model od room(Room) model. treba ga napisati malim mesage(to je zapravo Message model) i underscore _ set.  i all na kraju, daj nam sve
    participants = room.participants.all()
    
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room =i
    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html',context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)



@login_required(login_url='login') #ukoliko nema usera ne mozes napraviti createRoom, to je znjacenje ovog dekoratera i odvesti ce nas na login page
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        # form = RoomForm(request.POST)
        # if form.is_valid(): #ako je form validan, da su sva mjesta popunjena koja trebaju biti sto mozemo videti u forms.py
        #      room = form.save(commit=False) #to ce spremiti u databasu
        #      room.host = request.user
        #      room.save()
        return redirect('home') #i posalji nas na novu url stranicu home
    context = {'form': form, 'topics':topics}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login') #ukoliko nema usera ne mozes napraviti createRoom, to je znjacenje ovog dekoratera i odvesti ce nas na login page
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host: #only correct user can update it
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form, 'topics':topics, 'room':room}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login') #ukoliko nema usera ne mozes napraviti createRoom, to je znjacenje ovog dekoratera i odvesti ce nas na login page
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host: 
        return HttpResponse('Your are not allowed here!!')


    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':room})


@login_required(login_url='login') #ukoliko nema usera ne mozes napraviti createRoom, to je znjacenje ovog dekoratera i odvesti ce nas na login page
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user: 
        return HttpResponse('Your are not allowed here!!')


    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':message})

@login_required(login_url='login') #ukoliko nema usera ne mozes napraviti createRoom, to je znjacenje ovog dekoratera i odvesti ce nas na login page
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {'form':form}
    return render(request, 'base/update-user.html',context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics':topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request,'base/activity.html',{'room_messages':room_messages})
