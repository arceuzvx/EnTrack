from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum, Avg
import json
import random
from django.template.loader import render_to_string

from .models import UserProfile, EnergyData, LeaderboardEntry, Task
from .forms import UserRegisterForm, UserProfileForm, EnergyDataForm, TaskForm

# Energy saving tips
ENERGY_TIPS = [
    "Turn off lights when not in use to save electricity.",
    "Use LED bulbs instead of incandescent to reduce energy consumption by up to 80%.",
    "Unplug electronics when not in use to eliminate phantom energy usage.",
    "Set your thermostat 2 degrees lower in winter and higher in summer to reduce HVAC energy use.",
    "Wash clothes in cold water to save on water heating costs.",
    "Use a programmable thermostat to automatically adjust temperature when you're away or sleeping.",
    "Seal air leaks around windows and doors to improve heating and cooling efficiency.",
    "Clean or replace HVAC filters regularly to improve efficiency.",
    "Use natural light when possible instead of artificial lighting.",
    "Run dishwashers and washing machines only when full to maximize efficiency.",
    "Install low-flow showerheads to reduce hot water usage.",
    "Use power strips for electronics and turn them off when not in use.",
    "Keep your refrigerator coils clean to improve efficiency.",
    "Use ceiling fans to reduce the need for air conditioning.",
    "Air dry clothes instead of using a dryer when possible."
]

def home(request):
    """Home page view"""
    return render(request, 'dashboard/home.html')

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'dashboard/register.html', {'form': form})

@login_required
def dashboard(request):
    """Main dashboard view"""
    # Get user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get energy data
    energy_data = EnergyData.objects.filter(user=request.user).order_by('-date')[:6]
    
    # Get leaderboard data
    current_month = timezone.now().replace(day=1)
    leaderboard_entries = LeaderboardEntry.objects.filter(month=current_month).order_by('rank')[:10]
    
    # Get tasks
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    
    # Get random energy tip
    energy_tip = random.choice(ENERGY_TIPS)
    
    form = TaskForm()
    
    context = {
        'profile': profile,
        'energy_data': energy_data,
        'leaderboard_entries': leaderboard_entries,
        'tasks': tasks,
        'energy_tip': energy_tip,
        'form': form
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def energy_calculator(request):
    """Energy calculator view"""
    if request.method == 'POST':
        form = EnergyDataForm(request.POST)
        if form.is_valid():
            energy_data = form.save(commit=False)
            energy_data.user = request.user
            
            # Get previous month's data
            prev_month_data = EnergyData.objects.filter(
                user=request.user,
                date__lt=timezone.now()
            ).order_by('-date').first()
            
            if prev_month_data:
                # Calculate savings compared to previous month
                elec_saved = max(0, prev_month_data.electricity - energy_data.electricity)
                gas_saved = max(0, prev_month_data.gas - energy_data.gas)
                # Convert gas to kWh equivalent (1 therm ≈ 29.3 kWh)
                energy_data.saved = elec_saved + (gas_saved * 29.3)
            else:
                energy_data.saved = (energy_data.electricity * 0.1) + (energy_data.gas * 29.3 * 0.1)
            
            energy_data.save()
            
            # Update user profile total energy saved
            profile = request.user.profile
            profile.total_energy_saved += energy_data.saved
            profile.save()
            
            # Update or create leaderboard entry
            current_month = timezone.now().replace(day=1)
            LeaderboardEntry.objects.update_or_create(
                user=request.user,
                month=current_month,
                defaults={
                    'energy_saved': profile.total_energy_saved,
                    'co2_reduction': profile.get_co2_reduction()
                }
            )
            
            # Update leaderboard rankings
            update_leaderboard_rankings(current_month)

            messages.success(request, 'Energy data saved successfully!')
            
            return redirect('dashboard')
    else:
        form = EnergyDataForm()
    
    # Get random energy tip
    energy_tip = random.choice(ENERGY_TIPS)
    
    return render(request, 'dashboard/calculator.html', {'form': form, 'energy_tip': energy_tip})

@login_required
def user_settings(request):
    """User settings view"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    context = {
        'profile': profile,
    }
    
    return render(request, 'dashboard/settings.html', context)

@login_required
def update_profile(request):
    """Update user profile information"""
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        # Update user
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('user_settings')
    
    return redirect('user_settings')

@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_settings')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    
    return redirect('user_settings')

@login_required
def update_preferences(request):
    """Update user preferences"""
    if request.method == 'POST':
        profile = request.user.profile
        
        # Get form data
        profile.energy_unit = request.POST.get('energy_unit', 'kwh')
        profile.gas_unit = request.POST.get('gas_unit', 'therms')
        
        # Handle checkboxes
        profile.email_notifications = 'email_notifications' in request.POST
        profile.monthly_report = 'monthly_report' in request.POST
        profile.tips_notifications = 'tips_notifications' in request.POST
        
        profile.save()
        
        messages.success(request, 'Your preferences have been updated successfully!')
        return redirect('user_settings')
    
    return redirect('user_settings')

@login_required
def delete_account(request):
    """Delete user account"""
    if request.method == 'POST':
        user = request.user
        # Log the user out and delete their account
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('home')
    
    return redirect('user_settings')

@login_required
def energy_history(request):
    """Energy usage history view"""
    energy_data = EnergyData.objects.filter(user=request.user).order_by('-date')
    
    if request.method == 'POST':
        form = EnergyDataForm(request.POST)
        if form.is_valid():
            energy_data_entry = form.save(commit=False)
            energy_data_entry.user = request.user
            
            # Get previous month's data
            prev_month_data = EnergyData.objects.filter(
                user=request.user,
                date__lt=timezone.now()
            ).order_by('-date').first()
            
            if prev_month_data:
                # Calculate savings compared to previous month
                elec_saved = max(0, prev_month_data.electricity - energy_data_entry.electricity)
                gas_saved = max(0, prev_month_data.gas - energy_data_entry.gas)
                # Convert gas to kWh equivalent (1 therm ≈ 29.3 kWh)
                energy_data_entry.saved = elec_saved + (gas_saved * 29.3)
            else:
                energy_data_entry.saved = (energy_data_entry.electricity * 0.1) + (energy_data_entry.gas * 29.3 * 0.1)
            
            energy_data_entry.save()
            
            # Update user profile total energy saved
            profile = request.user.profile
            profile.total_energy_saved += energy_data_entry.saved
            profile.save()
            
            # Update or create leaderboard entry
            current_month = timezone.now().replace(day=1)
            LeaderboardEntry.objects.update_or_create(
                user=request.user,
                month=current_month,
                defaults={
                    'energy_saved': profile.total_energy_saved,
                    'co2_reduction': profile.get_co2_reduction()
                }
            )
            
            # Update leaderboard rankings
            update_leaderboard_rankings(current_month)

            messages.success(request, 'Energy data saved successfully!')
            return redirect('history')
    else:
        form = EnergyDataForm()
    
    return render(request, 'dashboard/history.html', {'energy_data': energy_data, 'form': form})

@login_required
def delete_energy_data(request, data_id):
    """Delete an energy data entry"""
    energy_data = get_object_or_404(EnergyData, id=data_id, user=request.user)
    
    if request.method == 'POST':
        # Subtract the saved energy from the user's total
        profile = request.user.profile
        profile.total_energy_saved = max(0, profile.total_energy_saved - energy_data.saved)
        profile.save()
        
        # Delete the entry
        energy_data.delete()
        
        # Update leaderboard entry
        current_month = timezone.now().replace(day=1)
        LeaderboardEntry.objects.update_or_create(
            user=request.user,
            month=current_month,
            defaults={
                'energy_saved': profile.total_energy_saved,
                'co2_reduction': profile.get_co2_reduction()
            }
        )
        
        # Update leaderboard rankings
        update_leaderboard_rankings(current_month)
        
        messages.success(request, 'Energy data entry deleted successfully!')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        
    return redirect('history')

@login_required
def get_energy_chart_data(request):
    """API endpoint for chart data"""
    # Get last 12 months of data
    end_date = timezone.now()
    start_date = end_date - timedelta(days=365)
    
    energy_data = EnergyData.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date')
    
    # Prepare data for charts
    labels = [data.date.strftime('%b %Y') for data in energy_data]
    electricity_data = [data.electricity for data in energy_data]
    gas_data = [data.gas for data in energy_data]
    saved_data = [data.saved for data in energy_data]
    
    chart_data = {
        'labels': labels,
        'electricity': electricity_data,
        'gas': gas_data,
        'saved': saved_data
    }
    
    return JsonResponse(chart_data)

@login_required
def add_task(request):
    """Add a new task"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                task_html = render_to_string('dashboard/task_item.html', {'task': task}, request=request)
                return JsonResponse({'new_task_html': task_html})
            return redirect('dashboard')
    return redirect('dashboard')

@login_required
def toggle_task(request, task_id):
    """Toggle task completion status"""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            task_html = render_to_string('dashboard/task_item.html', {'task': task}, request=request)
            return JsonResponse({'updated_task_html': task_html})
        return redirect('dashboard')
    return redirect('dashboard')

@login_required
def delete_task(request, task_id):
    """Delete a task"""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        return redirect('dashboard')
    return redirect('dashboard')

@login_required
def get_energy_tip(request):
    """Get a random energy saving tip"""
    tip = random.choice(ENERGY_TIPS)
    return JsonResponse({'tip': tip})

def update_leaderboard_rankings(month):
    """Update leaderboard rankings for a given month"""
    entries = LeaderboardEntry.objects.filter(month=month).order_by('-energy_saved')
    
    # Update ranks
    for i, entry in enumerate(entries, 1):
        entry.rank = i
        entry.save()
