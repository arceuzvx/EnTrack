from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='dashboard/logout.html'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('calculator/', views.energy_calculator, name='calculator'),
    path('settings/', views.user_settings, name='user_settings'),
    path('history/', views.energy_history, name='history'),
    path('api/chart-data/', views.get_energy_chart_data, name='chart_data'),
    path('task/add/', views.add_task, name='add_task'),
    path('task/<int:task_id>/toggle/', views.toggle_task, name='toggle_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('api/energy-tip/', views.get_energy_tip, name='energy_tip'),
    
    # New URL patterns for settings functionality
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/update-preferences/', views.update_preferences, name='update_preferences'),
    path('profile/delete-account/', views.delete_account, name='delete_account'),
] 