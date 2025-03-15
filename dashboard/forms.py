from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, EnergyData, Task

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'username', 'dark_mode', 'notifications', 'show_on_leaderboard',
            'energy_unit', 'gas_unit', 'email_notifications', 'monthly_report', 'tips_notifications'
        ]
        labels = {
            'username': 'Display Name',
            'dark_mode': 'Enable Dark Mode',
            'notifications': 'Enable Notifications',
            'show_on_leaderboard': 'Show on Leaderboard',
            'energy_unit': 'Energy Unit',
            'gas_unit': 'Gas Unit',
            'email_notifications': 'Receive Email Notifications',
            'monthly_report': 'Receive Monthly Energy Report',
            'tips_notifications': 'Receive Energy Saving Tips'
        }

class EnergyDataForm(forms.ModelForm):
    class Meta:
        model = EnergyData
        fields = ['electricity', 'gas']
        labels = {
            'electricity': 'Monthly Electricity Usage (kWh)',
            'gas': 'Natural Gas Usage (therms)'
        }
        widgets = {
            'electricity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter kWh'}),
            'gas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter therms'})
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['text']
        labels = {
            'text': ''
        }
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task'})
        } 