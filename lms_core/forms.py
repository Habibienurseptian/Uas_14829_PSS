from django import forms
from django.contrib.auth.models import User
from .models import CourseContent

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Validate password strength (optional)
        if len(password) < 6:
            raise forms.ValidationError('Password must be at least 6 characters long.')
        return password
    
class CompletionForm(forms.Form):
    content_id = forms.ModelChoiceField(queryset=CourseContent.objects.all(), label="Pilih Konten", widget=forms.Select)