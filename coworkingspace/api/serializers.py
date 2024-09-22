from rest_framework import serializers
from django.contrib.auth import get_user_model
from coworkingspace.models import (
    User, Location, Description, OperationalTimings, Capacity, WorkspaceForm,
    Amenity, MeetingRoom, PrivateOffice, Desk, FloorData, Mentorship, User
)

class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password', 'last_name', 'organization']

    def validate(self, data):
        user = get_user_model().objects.filter(email=data['email'].lower()).exists()
        if user:
            raise serializers.ValidationError({"email": "Email already exists."})
    
        data['username'] = data['first_name'].lower()
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'organization']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'location_name', 'unit_number', 'address_line1', 'address_line2', 'area', 'zip_code', 'city', 'country']

class DescriptionSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=True, required=False)
    
    class Meta:
        model = Description
        fields = ['id', 'name', 'opening_date', 'description', 'email', 'phone', 'website_url', 'image']

class OperationalTimingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationalTimings
        fields = ['id', 'opening_time', 'closing_time', 'is_saturday_open', 'is_sunday_open']

class CapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Capacity
        fields = ['id', 'desks', 'size', 'private_offices', 'floors']

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'category', 'workspace_id']
        read_only_fields =  ('workspace_id', )

class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = ['id', 'name', 'capacity', 'price', 'available', 'workspace_id']
        read_only_fields =  ('workspace_id', )

class PrivateOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateOffice
        fields = ['id', 'desks', 'price', 'duration', 'similar', 'workspace_id']
        read_only_fields =  ('workspace_id', )

class DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = ['id', 'duration', 'price', 'available', 'type', 'workspace_id']
        read_only_fields =  ('workspace_id', )

class FloorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorData
        fields = ['id', 'exec_rooms', 'meeting_rooms', 'desks', 'duration', 'price', 'similar', 'workspace_id']
        read_only_fields =  ('workspace_id', )

class MentorshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentorship
        fields = ['id', 'domain', 'mentors', 'workspace_id']
        read_only_fields =  ('workspace_id', )

class WorkspaceFormSerializer(serializers.ModelSerializer):
    description = DescriptionSerializer()
    location = LocationSerializer()
    operational_timings = OperationalTimingsSerializer()
    capacity = CapacitySerializer()

    amenities = serializers.SerializerMethodField()
    meeting_rooms = serializers.SerializerMethodField()
    price_desks = serializers.SerializerMethodField()
    price_private_offices = serializers.SerializerMethodField()
    price_floors = serializers.SerializerMethodField()
    mentorship = serializers.SerializerMethodField()

    class Meta:
        model = WorkspaceForm
        fields = ['id', 'description', 'location', 'operational_timings', 'capacity', 'amenities',
            'meeting_rooms',
            'price_desks',
            'price_private_offices',
            'price_floors',
            'mentorship', 'category']
        read_only_fields  = ("category", )
        
    def get_amenities(self, obj):
        amenities = Amenity.objects.filter(workspace_id=obj.pk)
        return AmenitySerializer(amenities, many=True).data

    def get_meeting_rooms(self, obj):
        meeting_rooms = MeetingRoom.objects.filter(workspace_id=obj.pk)
        return MeetingRoomSerializer(meeting_rooms, many=True).data

    def get_price_desks(self, obj):
        desks = Desk.objects.filter(workspace_id=obj.pk)
        return DeskSerializer(desks, many=True).data

    def get_price_private_offices(self, obj):
        private_offices = PrivateOffice.objects.filter(workspace_id=obj.pk)
        return PrivateOfficeSerializer(private_offices, many=True).data

    def get_price_floors(self, obj):
        floors = FloorData.objects.filter(workspace_id=obj.pk)
        return FloorDataSerializer(floors, many=True).data

    def get_mentorship(self, obj):
        mentorships = Mentorship.objects.filter(workspace_id=obj.pk)
        return MentorshipSerializer(mentorships, many=True).data
        
    
class AddWorkspaceFormSerializer(serializers.Serializer):
    description = DescriptionSerializer()
    location = LocationSerializer()
    operational_timings = OperationalTimingsSerializer()
    capacity = CapacitySerializer()

    amenities = AmenitySerializer(many=True, required=False)
    meeting_rooms = MeetingRoomSerializer(many=True, required=False)
    price_desks = DeskSerializer(many=True, required=False)
    price_private_offices = PrivateOfficeSerializer(many=True, required=False)
    price_floors = FloorDataSerializer(many=True, required=False)
    mentorship = MentorshipSerializer(many=True, required=False)

    class Meta:
        model  =  WorkspaceForm
        fields = ['id', 'description', 'location', 'operational_timings', 'capacity', 'amenities',
            'meeting_rooms',
            'price_desks',
            'price_private_offices',
            'price_floors',
            'mentorship',]
        
    def create(self, validated_data):
        user = self.context['request'].user
        description_data = validated_data.pop('description')
        location_data = validated_data.pop('location')
        operational_timings_data = validated_data.pop('operational_timings')
        capacity_data = validated_data.pop('capacity')
        amenities_data = validated_data.pop('amenities', [])
        meeting_rooms_data = validated_data.pop('meeting_rooms', [])
        price_desks_data = validated_data.pop('price_desks', [])
        price_private_offices_data = validated_data.pop('price_private_offices', [])
        price_floors_data = validated_data.pop('price_floors', [])
        mentorship_data = validated_data.pop('mentorship', [])

        description = Description.objects.create(**description_data)
        location = Location.objects.create(**location_data)
        operational_timings = OperationalTimings.objects.create(**operational_timings_data)
        capacity = Capacity.objects.create(**capacity_data)

        workspace_form = WorkspaceForm.objects.create(
            description=description,
            location=location,
            operational_timings=operational_timings,
            capacity=capacity,
            user=user
        )
        
        print("--------done here---------")
        # Create amenities
        for amenity_data in amenities_data:
            Amenity.objects.create(workspace_id=workspace_form, **amenity_data)

        # Create meeting rooms
        for room_data in meeting_rooms_data:
            MeetingRoom.objects.create(workspace_id=workspace_form, **room_data)

        # Create desks
        for desk_data in price_desks_data:
            Desk.objects.create(workspace_id=workspace_form, **desk_data)

        # Create private offices
        for private_office_data in price_private_offices_data:
            PrivateOffice.objects.create(workspace_id=workspace_form, **private_office_data)

        # Create floor data
        for floor_data in price_floors_data:
            FloorData.objects.create(workspace_id=workspace_form, **floor_data)

        # Create mentorship
        for mentorship_data in mentorship_data:
            Mentorship.objects.create(workspace_id=workspace_form, **mentorship_data)
        
        return workspace_form
    

class GetLocationsSerializer(serializers.Serializer):
    class Meta:
        model = Location
        fields = ['country', 'city',  'area']