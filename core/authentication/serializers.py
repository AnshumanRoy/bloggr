from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

def time_ago(time):
    now = timezone.now()
    time_diff = now - time
    seconds = time_diff.total_seconds()
    
    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif seconds < 3600:
        return f"{int(seconds/60)} minutes ago"
    elif seconds < 86400:
        return f"{int(seconds/3600)} hours ago"
    elif seconds < 2592000:
        return f"{int(seconds/86400)} days ago"
    elif seconds < 31536000:
        return f"{int(seconds/2592000)} months ago"
    else:
        return f"{int(seconds/31536000)} years ago"

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'confirm_password', 'profile_picture', 'bio')

    def validate(self, data):
        if User.objects.exists(email=data['email']):
            raise serializers.ValidationError("Account with this email already exists.")
        if User.objects.exists(username=data['username']):
            raise serializers.ValidationError("Account with this username already exists.")
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)
    
class BioUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('bio',)

class ProfilePictureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_picture',)

class UserProfileSerializer(serializers.ModelSerializer):
    profile_link = serializers.SerializerMethodField()

    def get_profile_link(self, obj):
        return reverse('user-profile', kwargs={'username': obj.username})

    class Meta:
        model = get_user_model()
        fields = ('username', 'profile_link')

class UserSerializer(serializers.ModelSerializer):
    time_since_joined = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'profile_picture',
            'bio',
            'time_since_joined'
        )
    
    def get_time_since_joined(self, obj):
        return time_ago(obj.date_joined)