from django import forms
from .models import CustomUser, Note

input_classes = "w-full bg-gray-50 dark:bg-gray-800 border-none rounded-2xl px-6 py-4 text-gray-900 dark:text-white placeholder:text-gray-400 focus:ring-2 focus:ring-blue-500 transition-all outline-none"

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': input_classes, 'placeholder': '••••••••'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': input_classes, 'placeholder': '••••••••'}), label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['fullname', 'email', 'password', 'confirm_password', 'mobile', 'city']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': input_classes, 'placeholder': 'john@example.com'}),
            'mobile': forms.TextInput(attrs={'class': input_classes, 'placeholder': '1234567890'}),
            'city': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'New York'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not mobile.isdigit() or len(mobile) < 10:
            raise forms.ValidationError("Enter a valid mobile number (at least 10 digits).")
        return mobile

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        return cleaned_data

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': input_classes, 'placeholder': 'Note Title'}),
            'content': forms.Textarea(attrs={'class': input_classes, 'rows': 5, 'placeholder': 'Write your note here...'}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['fullname', 'mobile', 'city']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': input_classes}),
            'mobile': forms.TextInput(attrs={'class': input_classes}),
            'city': forms.TextInput(attrs={'class': input_classes}),
        }
