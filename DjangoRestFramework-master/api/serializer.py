from rest_framework import serializers
from .models import Programmer


class ProgrammerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programmer
        # fields = ['id', 'fullname', 'nickname', 'age', 'is_active']
        fields = '__all__'
