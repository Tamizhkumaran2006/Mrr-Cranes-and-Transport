from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from functools import wraps
from .models import Post
from .forms import PostForm, LoginForm

# Decorator to check session-based login
def owner_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('owner_logged_in'):
            return redirect('blog:owner_login')
        return view_func(request, *args, **kwargs)
    return wrapper

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
    from django.core.mail import send_mail
    from .models import ContactMessage
    
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
                owner_email = 'mrrcranesandtransport@gmail.com'
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
                
                send_mail(
                    subject,
                    email_body,
                    'noreply@mrrcranesandtransport.com',
                    [owner_email],
                    fail_silently=False,
                )
                
                message = {'type': 'success', 'text': 'Thank you! Your inquiry has been received. We will contact you within 2 hours.'}
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
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        # Fixed credentials
        OWNER_USERNAME = "Rajaraman"
        OWNER_PASSWORD = "mrr_1981"

        # Check credentials
        if username == OWNER_USERNAME and password == OWNER_PASSWORD:
            # Set session
            request.session["owner_logged_in"] = True
            request.session.modified = True
            return redirect("blog:dashboard")
        else:
            # Show error
            context = {
                "error": "Invalid username or password. Please try again."
            }
            return render(request, "owner_login.html", context)

    return render(request, "owner_login.html")


# def owner_logout(request):
#     logout(request)
#     return redirect('blog:index')

def owner_logout(request):
    request.session.flush()   # Clear all session data
    return redirect('blog:index')


@owner_login_required
def dashboard(request):
    # Check login session
    if not request.session.get("owner_logged_in"):
        return redirect("blog:owner_login")

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

