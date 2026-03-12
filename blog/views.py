import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from functools import wraps
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test

from .models import Post, ContactMessage
from .forms import PostForm, LoginForm

def owner_login_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='/admin/login/')(view_func)

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
    message = None
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        service = request.POST.get('service', '').strip()
        project = request.POST.get('project', '').strip()
        date = request.POST.get('date', '').strip()
        
        if name and email and phone and service and project:
            try:
                # Save to database
                contact = ContactMessage.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    service=service,
                    project=project,
                    date=date if date else None
                )
                
                # Send email to owner
                owner_email = settings.ADMIN_EMAIL
                subject = f'New Quote Request from {name}'
                
                email_body = f"""
                New Quote Request Received!
                
                Customer Details:
                Name: {name}
                Email: {email}
                Phone: {phone}
                
                Service Required: {service}
                Preferred Date: {date if date else 'Not specified'}
                
                Project Details:
                {project}
                
                Please contact the customer within 2 hours to provide a quote.
                
                Best regards,
                MRR Cranes and Transport Website
                """
                
                try:
                    send_mail(
                        subject,
                        email_body,
                        settings.DEFAULT_FROM_EMAIL,
                        [owner_email],
                        fail_silently=False,
                    )
                    message = {'type': 'success', 'text': 'Thank you! Your inquiry has been received. We will contact you within 2 hours.'}
                except Exception as email_error:
                    logger = logging.getLogger(__name__)
                    logger.exception("Email sending failed")

                    error_text = 'Your inquiry was saved, but we could not send the email notification right now.'
                    if getattr(settings, 'DEBUG', False):
                        error_text = f"{error_text} Error: {str(email_error)}"
                    message = {'type': 'error', 'text': error_text}
            except Exception as e:
                message = {'type': 'error', 'text': f'Error: {str(e)}'}
        else:
            message = {'type': 'error', 'text': 'Please fill in all required fields.'}
    
    return render(request, 'contact.html', {
        'you_are_in': you_are_in, 
        'contact_num': contact_num,
        'message': message
    })

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
def owner_login(request):
    return redirect('/admin/login/?next=/owner/dashboard/')


# def owner_logout(request):
#     logout(request)
#     return redirect('blog:index')

def owner_logout(request):
    logout(request)
    return redirect('blog:index')


@owner_login_required
def dashboard(request):
    # Show all posts (because no Django user system)
    posts = Post.objects.all().order_by('-id')

    return render(request, 'dashboard.html', {'posts': posts})


@owner_login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog:dashboard')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@owner_login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:dashboard')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@owner_login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:dashboard')
    return render(request, 'delete_post.html', {'post': post})

def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)

