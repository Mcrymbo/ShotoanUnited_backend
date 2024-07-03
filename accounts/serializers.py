from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Profile, Account

# user serializer
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'username', 'first_name', 'last_name', 'is_deactivated', 'email', 'is_active']

# profile serializers
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'user', 'club',
                  'location', 'profile_pic',
                  'profile_pic_url', 'cover_photo',
                  'cover_photo_url', 'bio', 'phone_number', ]

# creating new users
User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'first_name', 'last_name',
                  'email', ]

    # you can grab the created user and do something with them here
    def create(self, validated_data):

        user = super().create(validated_data)

        return user

class UserSerializer(BaseUserSerializer):

    profile = serializers.SerializerMethodField()

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'first_name',
                  'last_name', 'email',
                  'username',
                  'is_active',
                  'is_deactivated',
                  'profile',
                  ]
    
    def get_profile(self, obj):
        profile = Profile.objects.filter(user=obj).first()
        if profile:
            return ProfileSerializer(profile).data
        return None

    # this is where we send a request to slash me/ or auth/users
    def validate(self, attrs):
        validated_attr = super().validate(attrs)
        username = validated_attr.get('username')

        user = User.objects.get(username=username)

        if user.is_deactivated:
            raise ValidationError(
                'Account deactivated')

        if not user.is_active:
            raise ValidationError(
                'Account not activated')

        return validated_attr

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        obj = self.user

        # you can do all sort of things here !!!
        # let me try something crazy if a user's last login is less than 2-minutes we deny
        # them access to the system 🤣🤣🤣🥲
        '''
        current_time = datetime.now()
        two_minutes_ago = current_time - timedelta(minutes=2)
        if obj.last_login > two_minutes_ago :
            raise ValidationError(
                'You are not allowed to login at this time wait for 2 minutes ')

        
        '''
        # if obj.is_deactivated:
        #     raise ValidationError(
        #         'Account deactivated. Account deactivated!!')

        # if not obj.is_active:
        #     raise ValidationError(
        #         'Account not activated. go to your email and activate your account')

        data.update({
            'id': obj.id, 'first_name': obj.first_name,
            'last_name': obj.last_name, 'email': obj.email,
            'username': obj.username,
            'is_active': obj.is_active,
            'is_deactivated': obj.is_deactivated,
        })

        return data