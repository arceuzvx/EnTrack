from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    ENERGY_UNIT_CHOICES = (
        ('kwh', 'Kilowatt-hour (kWh)'),
        ('mwh', 'Megawatt-hour (MWh)'),
    )
    
    GAS_UNIT_CHOICES = (
        ('therms', 'Therms'),
        ('cubic_feet', 'Cubic Feet'),
        ('cubic_meters', 'Cubic Meters'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=100, blank=True)
    dark_mode = models.BooleanField(default=False)
    notifications = models.BooleanField(default=True)
    show_on_leaderboard = models.BooleanField(default=True)
    total_energy_saved = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    # New fields for preferences
    energy_unit = models.CharField(max_length=10, choices=ENERGY_UNIT_CHOICES, default='kwh')
    gas_unit = models.CharField(max_length=15, choices=GAS_UNIT_CHOICES, default='therms')
    email_notifications = models.BooleanField(default=True)
    monthly_report = models.BooleanField(default=True)
    tips_notifications = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_co2_reduction(self):
        """Calculate CO2 reduction based on energy saved (kg)"""
        return self.total_energy_saved * 0.92
    
    def get_tree_equivalent(self):
        """Calculate tree equivalent (1 tree absorbs about 25kg CO2 per year)"""
        return self.get_co2_reduction() / 25

class EnergyData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='energy_data')
    date = models.DateField(default=timezone.now)
    electricity = models.FloatField(default=0)  # kWh
    gas = models.FloatField(default=0)  # therms
    saved = models.FloatField(default=0)  # kWh
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username}'s Energy Data - {self.date}"

class LeaderboardEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    month = models.DateField()  # Store the first day of the month
    energy_saved = models.FloatField(default=0)
    co2_reduction = models.FloatField(default=0)
    rank = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['rank', '-energy_saved']
        unique_together = ['user', 'month']
    
    def __str__(self):
        return f"{self.user.username}'s Leaderboard Entry - {self.month.strftime('%B %Y')}"
    
    def save(self, *args, **kwargs):
        # Calculate CO2 reduction if not provided
        if not self.co2_reduction and self.energy_saved:
            self.co2_reduction = self.energy_saved * 0.92
        super().save(*args, **kwargs)

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    text = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['completed', '-created_at']
    
    def __str__(self):
        return f"{self.text} - {self.user.username}"
