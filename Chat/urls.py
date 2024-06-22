
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login,name="login"),
    path('User/List',views.list_of_user,name="list_of_user"),
    path('chat/single/<int:other_user_id>/', views.single_chat, name='single_chat'),
    path('group/List',views.group_list,name="group_list"),
    path('chat/group/<str:group_name>/', views.group_chat, name='group_chat'),

    # ------------------- New Chat -----------------------
    path('Chat/',views.chat,name="chat"),
    path('get_single_chat_messages/',views.get_single_chat_messages,name="get_single_chat_messages"),


    # --------------------------- GROUP CHAT -------------------
    path('get_group_chat_messages/',views.get_group_chat_messages,name="get_group_chat_messages"),
    
]
