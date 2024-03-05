from datetime import timezone
from django import forms 
from tdlapp.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class Signup(UserCreationForm):
    display_name = forms.CharField(label="Enter Full Name", widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(label="Enter Username", widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label="Enter Email", widget=forms.EmailInput(attrs={'class':'form-control'}))
    user_type = forms.ChoiceField(label="Select User Type", choices=Custom_user.USER, widget=forms.Select(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="Enter Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    class Meta:
        model= Custom_user
        fields= ['display_name', 'username', 'email','user_type',]
        
        
class login_form(forms.Form):
    email = forms.EmailField(label="Enter Email", widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Enter Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'priority', 'is_completed')
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due_date'].required = False  

    # def clean_due_date(self):
    #     """Validate due date to be in the future (optional)."""
    #     due_date = self.cleaned_data.get('due_date')
    #     if due_date and due_date < timezone.now().date():
    #         raise forms.ValidationError("Due date cannot be in the past.")
    #     return due_date

    
    