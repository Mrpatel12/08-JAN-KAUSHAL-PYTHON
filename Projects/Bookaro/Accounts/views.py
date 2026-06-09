import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm, UserLoginForm, ContactForm, UserProfileForm, ProfilePictureForm
from .models import EmailOTP, UserProfile
from django.contrib.auth.models import User

from Services.models import Accommodation

def home(request):
    featured_accommodations = Accommodation.objects.all()[:4] # Get first 4 for the grid
    return render(request, 'home.html', {'featured_accommodations': featured_accommodations})

def about_view(request):
    return render(request, 'about.html')

def signup_view(request):
    print("DEBUG: SIGNUP VIEW ACCESSED")
    if request.method == 'POST':
        print("DEBUG: SIGNUP POST RECEIVED")
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate until OTP verified
            user.save()
            
            # Generate OTP
            otp = f"{random.randint(100000, 999999)}"
            EmailOTP.objects.update_or_create(user=user, defaults={'otp': otp})
            
            # Send Email (Console/SMTP)
            print("\n" + "="*50)
            print(f"   >>> YOUR OTP IS: {otp} <<<")
            print("="*50 + "\n")
            
            try:
                send_mail(
                    'Verify your Bookaro Account',
                    f'Your OTP for account verification is: {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                print(f"DEBUG: send_mail called for {user.email}")

                request.session['unverified_user_id'] = user.id
                messages.info(request, "Please enter the OTP sent to your email to verify your account.")
                return redirect('verify_otp')
            except Exception as e:
                print(f"ERROR sending OTP to {user.email}: {e}")
                messages.error(request, "Failed to send verification email. Please check email settings or try again later.")
                return redirect('signup')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def verify_otp_view(request):
    user_id = request.session.get('unverified_user_id')
    if not user_id:
        return redirect('signup')
    
    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '').strip()
        try:
            user = User.objects.get(id=user_id)
            otp_obj = EmailOTP.objects.get(user=user)
            
            if otp_obj.otp == otp_entered:
                user.is_active = True
                user.save()
                otp_obj.delete()
                
                # Specify backend to avoid AttributeError when logging in manually fetched user
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                del request.session['unverified_user_id']
                messages.success(request, f"Welcome to Bookaro, {user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid OTP. Please try again.")
        except User.DoesNotExist:
            messages.error(request, "User session invalid. Please log in again.")
            return redirect('login')
        except EmailOTP.DoesNotExist:
            messages.error(request, "OTP expired or not found. Please request a new one.")
            return redirect('verify_otp')
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            return redirect('login')
            
    return render(request, 'accounts/verify_otp.html')

def login_view(request):
    print("DEBUG: LOGIN VIEW ACCESSED")
    if request.method == 'POST':
        print("DEBUG: LOGIN POST RECEIVED")
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            try:
                user_obj = User.objects.get(email=email)
                # Check if user is active or needs verification
                user = authenticate(username=user_obj.username, password=password)
                
                if user is None and not user_obj.is_active:
                    # Check password manually for inactive users to trigger verification
                    if user_obj.check_password(password):
                        user = user_obj
                    else:
                        messages.error(request, "Invalid username or password.")
                        return render(request, 'accounts/login.html', {'form': form})
                
                if user is not None:
                    # Generate and Send OTP for 2FA or Activation
                    otp = f"{random.randint(100000, 999999)}"
                    EmailOTP.objects.update_or_create(user=user, defaults={'otp': otp})
                    
                    subject = 'Your Bookaro Verification Code'
                    message = f'Your verification code is: {otp}'
                    if not user.is_active:
                        subject = 'Verify your Bookaro Account'
                        message = f'Your OTP for account verification is: {otp}'
                    
                    print("\n" + "="*50)
                    print(f"   >>> YOUR OTP IS: {otp} <<<")
                    print("="*50 + "\n")
                    
                    try:
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            [user.email],
                            fail_silently=False,
                        )
                        print(f"DEBUG: send_mail called for {user.email}")

                        request.session['unverified_user_id'] = user.id
                        messages.info(request, "A verification code has been sent to your email.")
                        return redirect('verify_otp')
                    except Exception as e:
                        print(f"ERROR sending OTP to {user.email}: {e}")
                        messages.error(request, "Failed to send verification email. Please check email settings or try again later.")
                        return redirect('login')
                else:
                    messages.error(request, "Invalid username or password.")
            except User.DoesNotExist:
                messages.error(request, "Invalid username or password.")
            except User.MultipleObjectsReturned:
                messages.error(request, "Multiple accounts found with this email. Please contact support.")
            except Exception as e:
                print(f"DEBUG ERROR: {str(e)}")
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def resend_otp_view(request):
    user_id = request.session.get('unverified_user_id')
    if not user_id:
        messages.error(request, "Session expired. Please log in or sign up again.")
        return redirect('login')
    
    try:
        user = User.objects.get(id=user_id)
        otp = f"{random.randint(100000, 999999)}"
        EmailOTP.objects.update_or_create(user=user, defaults={'otp': otp})
        
        try:
            send_mail(
                'Your New Bookaro Verification Code',
                f'Your new verification code is: {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, "A new verification code has been sent to your email.")
        except Exception as e:
            print(f"ERROR resending OTP to {user.email}: {e}")
            messages.error(request, "Failed to resend verification email. Please try again later.")
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')
    
    return redirect('verify_otp')

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been sent and stored successfully.")
            return redirect('contact')
        else:
            messages.error(request, "Please fix the errors in the form.")
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

@login_required
def edit_profile_view(request):
    # Ensure profile exists for users created before the signal was added
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('edit_profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = ProfilePictureForm(instance=profile)
    
    return render(request, 'accounts/edit_profile.html', {
        'form': user_form,
        'profile_form': profile_form
    })
