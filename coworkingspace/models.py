from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    organization = models.CharField(max_length=50, blank=True, null=True)

# Location model
class Location(models.Model):
    location_name = models.CharField(max_length=255)
    unit_number = models.CharField(max_length=10)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"Location: {self.location_name}, {self.city}, {self.country}"

# Description model
class Description(models.Model):
    name = models.CharField(max_length=255)
    opening_date = models.DateField()
    description = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='workspace_images/', blank=True, null=True)

    def __str__(self):
        return self.name

# Operational timings model
class OperationalTimings(models.Model):
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_saturday_open = models.BooleanField(default=False)
    is_sunday_open = models.BooleanField(default=False)

    def __str__(self):
        return f"Opening: {self.opening_time}, Closing: {self.closing_time}"

# Capacity model
class Capacity(models.Model):
    desks = models.PositiveIntegerField()
    size = models.CharField(max_length=50)
    private_offices = models.PositiveIntegerField()
    floors = models.PositiveIntegerField()

    def __str__(self):
        return f"Capacity: {self.desks} desks, {self.size}"

# Main form data model
class WorkspaceForm(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.OneToOneField(Description, on_delete=models.CASCADE)
    location = models.OneToOneField(Location, on_delete=models.CASCADE) 
    operational_timings = models.OneToOneField(OperationalTimings, on_delete=models.CASCADE)
    capacity = models.OneToOneField(Capacity, on_delete=models.CASCADE)

    def __str__(self):
        return f"Workspace Form by {self.user.username}"
    

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    workspace_id = models.ForeignKey(WorkspaceForm, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.category})"
    

# Meeting room model
class MeetingRoom(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    workspace_id = models.ForeignKey(WorkspaceForm, on_delete=models.CASCADE)

    def __str__(self):
        return f"Meeting Room: {self.name} with capacity {self.capacity}"
    

# Private office model
class PrivateOffice(models.Model):
    desks = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=10, default='month')
    similar = models.CharField(max_length=100, blank=True, null=True)
    workspace_id = models.ForeignKey(WorkspaceForm, on_delete=models.CASCADE)

    def __str__(self):
        return f"Private Office: {self.desks} desks at ${self.price}"
    

# Desks model for hot and dedicated desks
class Desk(models.Model):
    DURATION_CHOICES = [
        ('day', 'Day'),
        ('month', 'Month'),
        ('year', 'Year')
    ]
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    type = models.CharField(max_length=50, choices=[('hot_desks', 'Hot Desks'), ('dedicated_desks', 'Dedicated Desks')])
    workspace_id = models.ForeignKey(WorkspaceForm, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.duration} desk at ${self.price}"
    

# Floor data model
class FloorData(models.Model):
    exec_rooms = models.PositiveIntegerField()
    meeting_rooms = models.PositiveIntegerField()
    desks = models.PositiveIntegerField()
    duration = models.CharField(max_length=10, default='month')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    similar = models.CharField(max_length=100, blank=True, null=True)
    workspace_id = models.ForeignKey(WorkspaceForm, on_delete=models.CASCADE)

    def __str__(self):
        return f"Floor: {self.exec_rooms} exec rooms, {self.meeting_rooms} meeting rooms"

# Mentorship model
class Mentorship(models.Model):
    domain = models.CharField(max_length=50)
    mentors = models.CharField(max_length=255)
    workspace_id = models.ForeignKey(WorkspaceForm, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"Mentorship in {self.domain} by {self.mentors}"
