from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import TODOSerializer
from .permissions import IsOwner

from icecream import ic
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    """
    Hiển thị danh sách các task

    """

    model = Task
    template_name = 'base/taks_list.html'  
    context_object_name = 'tasks'

    # Nếu cmt 2 dòng này và un cmt def ở dưới đó thì lại xử lý đc phần khác

    # paginate_by = 10
    # queryset = Task.objects.all() 
     

    
    
    def get_context_data(self, **kwargs):

        

        context = super(TaskList,self).get_context_data(**kwargs)
        ic(type(context))
        


        context['tasks'] = (context['tasks']).filter(user=self.request.user)
        # context['task'] = Task.objects.all()[:5].filter(user=self.request.user)
        ic((context['tasks']))
        context['count'] = context['tasks'].filter(complete=False).count()
         # context['count'] = Task.objects.all()[:5]
        ic((context['count']))
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        
        
        # list_task = Task.objects.all()
        # paginator = Paginator(list_task,self.paginate_by)
        # page = self.request.GET.get('page')
        # try:
        #     search_input = paginator.page(page)
        # except PageNotAnInteger:
        #     search_input = paginator.page(1)
        # except EmptyPage:
        #     search_input = paginator.page(paginator.num_pages)
        
        context['search_input'] = search_input
        return context

        
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))


class TODOListView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TODOSerializer
    permission_classes = (IsAuthenticated, )

class TODODetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TODOSerializer
    permission_classes = (IsOwner, )


    """
    -account user:
    anhkun1904
    co19042002
    
    -account admin:
    tuananh123
    co19042002
    """