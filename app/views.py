from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login
# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import chat_Group
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
             
            auth_login(request, user)
            return redirect('chat')
        else:
            messages.error(request, 'Invalid username or password.')
        
    return render(request,'login.html')
    

def list_of_user(request):
    users = User.objects.exclude(id=request.user.id)
    chat_groups = chat_Group.objects.filter(members=request.user)
    print("dddddddd",chat_groups)
    return render(request,'list_of_user.html',{'users': users,'chat_groups': chat_groups})


@login_required
def single_chat(request, other_user_id):
    other_user = User.objects.get(id=other_user_id)
    return render(request, 'single_chat.html',  {'other_user_id': other_user_id, 'other_user': other_user,'user':request.user})

def group_list(request):
    if request.user.is_authenticated:
        chat_groups = chat_Group.objects.filter(members=request.user)
    else:
        chat_groups = chat_Group.objects.none()
    return render(request,'group_list.html',{'chat_groups': chat_groups})


@login_required
def group_chat(request, group_name):
    group_name = chat_Group.objects.get(name=group_name)
   
    return render(request, 'group_chat.html', {'group_name': group_name,'user':request.user})




# def chat(request):
#     users = User.objects.exclude(id=request.user.id)
#     user = request.user.id
#     all_msg = ChatMessage.objects.all()
#     context = {
#         'users':users,
#         'user':user,
#         'all_msg':all_msg,
#     }
#     return render(request,'Chat/chat2.html',context)
from django.db.models import Q
from django.db.models import Q

def chat(request):
    users = User.objects.exclude(id=request.user.id)
    user = request.user.id

    # Initialize an empty dictionary to store messages
    all_messages = {}

    for u in users:
        # Fetch all messages for each user conversation, ordered by msg_time
        messages = ChatMessage.objects.filter(
            Q(message_by=request.user, receive_by=u) | Q(message_by=u, receive_by=request.user)
        ).order_by('msg_time')
        print(messages)

        # # Store all messages in a list for the user
        # if messages.exists():
        #     all_messages[u.id] = list(messages.values_list('message', flat=True))
    
    
    context = {
        'users': users,
        'user': user,
        'all_messages': all_messages,
    }
    return render(request, 'Chat/chat2.html', context)


from django.template import loader
from django.http import HttpResponse
from .models import ChatMessage
from django.db.models import Q
def get_single_chat_messages(request):
    user_id = request.GET.get("user_id")
    other_user_id = User.objects.get(id=user_id)
    user = request.user
    
    # Filter chat messages between the two users
    # msg_All = ChatMessage.objects.filter(message_by=other_user_id,receive_by=user)
    msg_all = ChatMessage.objects.filter(
        Q(message_by=user, receive_by=other_user_id) | 
        Q(message_by=other_user_id, receive_by=user)
    ).order_by('msg_time')

    # receiver_msg = ChatMessage.objects.filter(receive_by=user)
    
    
    
    context = {
        'other_user_id': other_user_id,
        'user': user,
        'msg_All': msg_all,
        # 'sender_msg': sender_msg,
        # 'receiver_msg': receiver_msg,
    }

   

    chat_content = loader.render_to_string("Chat/chat_content.html",context)
    return HttpResponse(chat_content)



def get_group_chat_messages(request):
    chat_content = loader.render_to_string("Chat/groupchat.html")
    return HttpResponse(chat_content)