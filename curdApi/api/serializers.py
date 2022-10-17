from rest_framework import serializers
from .models import Person

class PersonSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length= 100)
    last_name = serializers.CharField(max_length = 100)
    age = serializers.IntegerField()

    def create(self, validated_data):
        return Person.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance