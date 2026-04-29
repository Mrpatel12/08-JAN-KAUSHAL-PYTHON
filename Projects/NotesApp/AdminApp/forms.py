from django import forms
from UserApp.models import CustomUser

class AdminUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text="Leave blank to keep current password if editing.")

    class Meta:
        model = CustomUser
        fields = ['fullname', 'email', 'mobile', 'city', 'is_verified', 'is_active']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-lg border dark:bg-gray-800 dark:border-gray-700 dark:text-white'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 rounded-lg border dark:bg-gray-800 dark:border-gray-700 dark:text-white'}),
            'mobile': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-lg border dark:bg-gray-800 dark:border-gray-700 dark:text-white'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-lg border dark:bg-gray-800 dark:border-gray-700 dark:text-white'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'rounded text-blue-600'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded text-blue-600'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
