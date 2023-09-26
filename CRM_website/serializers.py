from rest_framework import serializers
from .models import Record


class RecordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Record
        # fields = ("first_name", "last_name", "phone", "email", "country", "city", "address",)
        fields = "__all__"
