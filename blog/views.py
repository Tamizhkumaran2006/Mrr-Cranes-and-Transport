from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from .models import Post
from .forms import PostForm, LoginForm

def index(request):
    you_are_in = "HOME"
    return render(request, 'index.html', {'you_are_in': you_are_in})

def about(request):
    you_are_in = "ABOUT US"
    return render(request, 'about.html', {'you_are_in': you_are_in})

def blog(request):
    you_are_in = "BLOG"
    posts = Post.objects.all()
    return render(request, 'blog.html', {'you_are_in': you_are_in, 'posts': posts})

def location(request):
    you_are_in = "LOCATION"
    return render(request, 'location.html', {'you_are_in': you_are_in})

def contact(request):
    contact_num = '9841099558'
    you_are_in = "CONTACT US"
    return render(request, 'contact.html', {'you_are_in': you_are_in, 'contact_num': contact_num})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'detail.html', {'post': post})

# def owner_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('blog:dashboard')
#             else:
#                 form.add_error(None, 'Invalid username or password')
#     else:
#         form = LoginForm()
#     return render(request, 'owner_login.html', {'form': form})

def owner_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Your fixed credentials
        OWNER_USERNAME = "Rajaraman"
        OWNER_PASSWORD = "mrr_1981"

        if username == OWNER_USERNAME and password == OWNER_PASSWORD:
            request.session["owner_logged_in"] = True
            return redirect("blog:dashboard")
        else:
            error_message = "Invalid username or password"
            return render(request, "owner_login.html", {"error": error_message})

    return render(request, "owner_login.html")


# def owner_logout(request):
#     logout(request)
#     return redirect('blog:index')

def owner_logout(request):
    request.session.flush()   # Clear all session data
    return redirect('blog:index')


@login_required(login_url='blog:owner_login')
# def dashboard(request):
#     posts = Post.objects.filter(author=request.user)
#     return render(request, 'dashboard.html', {'posts': posts})

def dashboard(request):
    # Check login session
    if not request.session.get("owner_logged_in"):
        return redirect("blog:owner_login")

    # Show all posts (because no Django user system)
    posts = Post.objects.all().order_by('-id')

    return render(request, 'dashboard.html', {'posts': posts})


@login_required(login_url='blog:owner_login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:dashboard')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required(login_url='blog:owner_login')
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:dashboard')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required(login_url='blog:owner_login')
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:dashboard')
    return render(request, 'delete_post.html', {'post': post})

def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)

