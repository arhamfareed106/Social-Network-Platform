from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatRoom

# Create your views here.

@login_required
def chat_home(request):
    if request.method == 'POST':
        participants = request.POST.getlist('participants')
        if participants:
            room = ChatRoom.objects.create()
            room.participants.add(request.user)
            room.participants.add(*participants)
            return redirect('chat-room', room_id=room.id)
    
    rooms = ChatRoom.objects.filter(participants=request.user)
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/home.html', {'rooms': rooms, 'users': users})

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in room.participants.all():
        return redirect('chat')
    return render(request, 'chat/room.html', {'room': room})
