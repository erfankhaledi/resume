from typing import Any
from django.db import models
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views import generic
from django.contrib import messages
from .models import Post
from .forms import PostForm
from .filters import PostFilter

def home(request):
    posts = Post.objects.filter(active=True, featured=True)[0:3]
    
    context = {'posts':posts}
    return render(request, "base/index.html", context)



def posts(request):
    posts = Post.objects.filter(active=True)
    myFilter = PostFilter(request.GET, queryset=posts)
    posts = myFilter.qs

    page = request.GET.get('page')
    paginator = Paginator(posts, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'myFilter': myFilter}
    return render(request, "base/posts.html", context)

class PostDetail(generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'base/post.html'
def post(request, slug):
    post = Post.objects.get(id=slug)
    context = {'post': post}
    return render(request, "base/post.html", context)

def profile(request):
    return render(request, "base/profile.html")

@login_required(login_url="home")
def create_post(request):
    form = PostForm(request.POST, request.FILES)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('base:posts')

    context = {'form':form}
    return render(request, "base/post_form.html", context)



class LeadUpdateView(generic.UpdateView):
    template_name = "base/post_form.html"
    context_object_name = 'form'
    form_class = PostForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        return Post.objects.filter(active=True)

    def get_success_url(self):
        return reverse("base:posts")

    # def form_valid(self, form):
    #     form.save()
    #     messages.info(self.request, "You have successfully updated this lead")
    #     return super(LeadUpdateView, self).form_valid(form)

@login_required(login_url="home")
def update_post(request, slug):
    post = Post.objects.get(id=slug)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('base:posts')

    context = {'form':form}
    return render(request, "base/post_form.html", context)

@login_required(login_url="home")
def delete_post(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        post.delete()
        return redirect('base:posts')
    context = {'item':post}
    return render(request, "base/post_delete.html", context)

