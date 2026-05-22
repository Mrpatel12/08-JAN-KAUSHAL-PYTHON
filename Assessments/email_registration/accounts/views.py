import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .forms import RegistrationForm


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_number')
            sms_text = f"Hello {user.username}, thank you for registering! Your account has been successfully created."

            # Fast2SMS Integration
            api_key = getattr(settings, 'FAST2SMS_API_KEY', None)
            if api_key and api_key.strip():
                url = "https://www.fast2sms.com/dev/bulkV2"
                payload = {
                    "route": "q",
                    "message": sms_text,
                    "language": "english",
                    "numbers": phone_number,
                }
                headers = {
                    "authorization": api_key,
                }
                try:
                    response = requests.post(url, data=payload, headers=headers)
                    print(f"[Fast2SMS Response] {response.status_code} - {response.text}")
                except Exception as exc:
                    print(f"[Fast2SMS Error] Failed to connect to API: {exc}")
            else:
                # Console Fallback for local development/testing
                print("\n" + "="*60)
                print("================ MOCK SMS SENT (CONSOLE FALLBACK) ================")
                print(f"To: +91 {phone_number}")
                print(f"Message: {sms_text}")
                print("="*60 + "\n")

            # Store phone number in session to render in success page
            request.session['registered_phone'] = phone_number
            messages.success(request, "Registration successful! A confirmation SMS has been sent.")
            return redirect("accounts:success")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


def success(request):
    phone_number = request.session.get('registered_phone', '')
    # Mask part of the number for privacy, e.g. XXXXXX1234
    masked_phone = f"XXXXXX{phone_number[-4:]}" if len(phone_number) >= 4 else phone_number
    return render(request, "accounts/success.html", {"phone": masked_phone})
