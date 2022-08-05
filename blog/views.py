from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import post, comment
from .forms import CommentForm
from community.settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail
from django.http import HttpResponse

def Email(request,emailto):
   res = send_mail("hello paul", "comment tu vas?", "wefey15970@ibrilo.com", [emailto])#adkmrs2020@gmail.com
   return HttpResponse('%s'%res)

def home(request):
    context = {'posts': post.objects.all()}
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by=4


class UserPostListView(ListView):
    model = post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 4
    

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = post 


def PostDetail(request, pk):
    p = post.objects.get(pk=pk)
    comments = p.comments
    # cnt = comments.count()
    new_comment = None
    form=CommentForm()
    blankForm = form
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = p
            new_comment.save()
        else:
            form = CommentForm()
        return render(request, 'blog/post_detail.html', {'form':blankForm, 'object':p, 'comment':comments})
    return render(request, 'blog/post_detail.html', {'form':blankForm, 'object':p, 'comment':comments})

# Create your views here.
#DataFlair #Send Email
# def subscribe(request):
#     sub = forms.Subscribe()
#     if request.method == 'POST':
#         sub = forms.Subscribe(request.POST)
#         subject = 'Welcome to DataFlair'
#         message = 'Hope you are enjoying your Django Tutorials'
#         recepient = str(sub['Email'].value())
#         send_mail(subject, 
#             message, EMAIL_HOST_USER, [recepient], fail_silently = False)
#         return render(request, 'blog/success.html', {'recepient': recepient})
#     return render(request, 'blog/base.html', {'form':sub})

class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def contact(request):
    return render(request, 'blog/contact.html', {'title': 'Contact Us'})