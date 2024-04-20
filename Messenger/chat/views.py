from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .forms import CreateChatForm
from .models import Chat, Message, User
from .permissions import IsOwnerOrReadOnly
from .serializers import ChatSerializer, UserSerializer


class ChatList(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'chat/chat_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        if self.request.path == reverse_lazy('chats'):
            return Chat.objects.filter(type=Chat.GROUP)
        elif self.request.path == reverse_lazy('user_chats'):
            return Chat.objects.filter(participants__has_key=str(self.request.user.pk))


class ChatDetail(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Chat
    template_name = 'chat/chat_detail.html'
    context_object_name = 'chat'

    def test_func(self):
        if self.request.user == self.get_object().creator:
            return True
        elif str(self.request.user.pk) in self.get_object().participants:
            return True
        return False


class CreateChat(LoginRequiredMixin, CreateView):
    model = Chat
    form_class = CreateChatForm
    template_name = 'chat/add_chat.html'

    def form_valid(self, form):
        chat = form.save(commit=False)
        chat.creator = self.request.user
        chat.add_participant(self.request.user)
        if self.request.path == reverse_lazy('add_personal_chat'):
            chat.type = Chat.PERSONAL
            to_user = User.objects.get(pk=self.request.GET.get('to'))
            chat.add_participant(to_user)
        elif self.request.path == reverse_lazy('add_group_chat'):
            chat.type = Chat.GROUP

        return super().form_valid(form)


class EditChat(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ['chat.change_chat']
    model = Chat
    form_class = CreateChatForm
    template_name = 'chat/edit_chat.html'

    def test_func(self):
        if self.request.user == self.get_object().creator:
            self.permission_required = []
            return True
        elif self.request.user.has_perms(self.permission_required):
            return True
        return False


class DeleteChat(UserPassesTestMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ['chat.delete_chat']
    model = Chat
    template_name = 'chat/delete_chat.html'

    def test_func(self):
        if self.request.user == self.get_object().creator:
            self.permission_required = []
            return True
        elif self.request.user.has_perms(self.permission_required):
            return True
        return False


@login_required
@csrf_protect
def manage_participants(request):
    if request.method == 'POST':
        user = request.user
        action = request.POST.get('action')
        chat_pk = request.POST.get('chat_pk')
        chat = Chat.objects.get(pk=chat_pk)

        if action == 'join':
            chat.add_participant(user)
            return redirect('chat', pk=chat_pk)
        elif action == 'leave':
            chat.remove_participant(user)
            return redirect('chats')
        elif action == 'delete':
            chat.delete()
            return redirect('chats')
        elif action == 'user_chats_delete':
            chat.delete()
            return redirect('user_chats')


class ChatGroupViewSet(ModelViewSet):
    queryset = Chat.objects.filter(type=Chat.GROUP)
    serializer_class = ChatSerializer

    def get_permissions(self):
        if self.request.user.is_staff:
            self.permission_classes = [IsAuthenticated]
            return [permission() for permission in self.permission_classes]
        elif self.action in ('create', 'retrieve', 'list'):
            self.permission_classes = [IsAuthenticated]
        elif self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        creator = self.request.user
        kwargs = {
            'creator': creator,
            'type': Chat.GROUP,
            'participants': {creator.pk: ''},
        }
        serializer.save(**kwargs)


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ('list',):
            self.permission_classes = [IsAuthenticated]
        elif self.action in ('retrieve', 'update', 'partial_update'):
            self.permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in self.permission_classes]



