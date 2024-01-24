from rest_framework import serializers
from .models import Property, Units, TenentRentAggriment, Documents,UserTable

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = '__all__'

class TenentRentAggrimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenentRentAggriment
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'

class UserTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = '__all__'
