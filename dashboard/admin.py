from django.contrib import admin
from .models import UserProfile, EnergyData, LeaderboardEntry, Task

# Register models
admin.site.register(UserProfile)
admin.site.register(EnergyData)
admin.site.register(LeaderboardEntry)
admin.site.register(Task)