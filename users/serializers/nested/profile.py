from rest_framework import serializers
from users.models.profile import Profile

class ProfileShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'telegram_id',
        )

class ProfileUpdatetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'telegram_id',
        )