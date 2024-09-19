from django.contrib import admin
from .models import (
    Location, Description, OperationalTimings, Capacity, WorkspaceForm, Amenity, 
    MeetingRoom, PrivateOffice, Desk, FloorData, Mentorship, User
)


# Register Location model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'organization')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')


# Register Location model
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'city', 'country')

# Register Description model
@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'opening_date', 'email', 'phone')

# Register OperationalTimings model
@admin.register(OperationalTimings)
class OperationalTimingsAdmin(admin.ModelAdmin):
    list_display = ('opening_time', 'closing_time', 'is_saturday_open', 'is_sunday_open')

# Register Capacity model
@admin.register(Capacity)
class CapacityAdmin(admin.ModelAdmin):
    list_display = ('desks', 'size', 'private_offices', 'floors')

# Register WorkspaceForm model
@admin.register(WorkspaceForm)
class WorkspaceFormAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'location', 'operational_timings', 'capacity')

# Register Amenity model
@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'workspace_id')

# Register MeetingRoom model
@admin.register(MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'price', 'available', 'workspace_id')

# Register PrivateOffice model
@admin.register(PrivateOffice)
class PrivateOfficeAdmin(admin.ModelAdmin):
    list_display = ('desks', 'price', 'duration', 'similar', 'workspace_id')

# Register Desk model
@admin.register(Desk)
class DeskAdmin(admin.ModelAdmin):
    list_display = ('duration', 'price', 'available', 'type', 'workspace_id')

# Register FloorData model
@admin.register(FloorData)
class FloorDataAdmin(admin.ModelAdmin):
    list_display = ('exec_rooms', 'meeting_rooms', 'desks', 'duration', 'price', 'similar', 'workspace_id')

# Register Mentorship model
@admin.register(Mentorship)
class MentorshipAdmin(admin.ModelAdmin):
    list_display = ('domain', 'mentors', 'workspace_id')
