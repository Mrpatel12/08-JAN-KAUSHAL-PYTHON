import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import CustomUser, OTP, Note
from .forms import SignupForm, NoteForm, UserUpdateForm

# Static Pages
def home(request):
    return render(request, 'UserApp/home.html')

def about(request):
    return render(request, 'UserApp/about.html')

def blog(request):
    return render(request, 'UserApp/blog.html')

def contact(request):
    return render(request, 'UserApp/contact.html')

# Signup
def signup(request):
    form = SignupForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.username = user.email
        user.set_password(form.cleaned_data['password'])
        user.save()

        otp = str(random.randint(100000, 999999))
        OTP.objects.create(user=user, otp=otp)

        from django.conf import settings
        send_mail(
            'Your OTP Code',
            f'Your OTP is {otp}',
            settings.EMAIL_HOST_USER,
            [user.email],
        )

        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('dashboard')
    elif request.method == 'POST':
        messages.error(request, 'Please correct the errors below.')

    return render(request, 'UserApp/signup.html', {'form': form})


# OTP Verification
def verify_otp(request):
    if request.method == "POST":
        otp_input = request.POST.get('otp')
        
        if request.user.is_authenticated:
            user = request.user
        elif 'user_id' in request.session:
            user = CustomUser.objects.get(id=request.session['user_id'])
        else:
            messages.error(request, 'Session expired. Please log in again.')
            return redirect('login')

        otp_obj = OTP.objects.filter(user=user, otp=otp_input).last()

        if otp_obj:
            user.is_verified = True
            user.save()
            messages.success(request, 'Account verified successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid or expired OTP. Please try again.')

    return render(request, 'UserApp/otp_verify.html')


# Login
def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.fullname}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'UserApp/login.html')


# Dashboard
@login_required(login_url='login')
def dashboard(request):
    notes = Note.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'UserApp/dashboard.html', {'notes': notes})

# Create Note
@login_required(login_url='login')
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('dashboard')
    else:
        form = NoteForm()
    return render(request, 'UserApp/note_form.html', {'form': form, 'action': 'Create'})

# Edit Note
@login_required(login_url='login')
def edit_note(request, pk):
    note = Note.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = NoteForm(instance=note)
    return render(request, 'UserApp/note_form.html', {'form': form, 'action': 'Edit'})

# Delete Note
@login_required(login_url='login')
def delete_note(request, pk):
    note = Note.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('dashboard')
    return render(request, 'UserApp/note_delete.html', {'note': note})


# Logout
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def send_verification_otp(request):
    user = request.user
    otp = str(random.randint(100000, 999999))
    OTP.objects.create(user=user, otp=otp)

    from django.conf import settings
    try:
        send_mail(
            'Your Verification Code',
            f'Your verification code is {otp}',
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        messages.success(request, 'A new verification code has been sent to your email.')
    except Exception as e:
        messages.error(request, 'Failed to send email. Please try again later.')
    
    return redirect('verify_otp')

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'UserApp/profile.html', {'form': form})
