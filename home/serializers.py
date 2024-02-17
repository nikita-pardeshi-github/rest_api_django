from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User
import re


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    # we use serializer class when we want to write whole custom logic.
    # for validation


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = ['color_name', 'id']


class PersonSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    col_info = serializers.SerializerMethodField()

    class Meta:
        # which model to serialize
        model = Person
        # what field to be serialized
        fields = '__all__'
        # depth = 1 # it will give you id and fields value of foreign key
    #
    # def validate(self, data):
    #     if data['age'] < 18:
    #         raise serializers.ValidationError('age should be greater than eighteen')
    #
    #     if re.search('[^a-zA-Z]+', data['name']):
    #         raise serializers.ValidationError('name should not contain any special character')
    #
    #     return data

    def validate_age(self, data):
        if data < 18:
            raise serializers.ValidationError('age should be greater than eighteen')
        return data

    def validate_name(self, data):
        print(f"In validate name : {data}")
        if re.search('[^a-zA-Z]+', data):
            raise serializers.ValidationError('name should not contain any special character')
        return data

    def get_col_info(self, obj):
        # obj is Person obj
        col_hex_dict = {'green':  '# 008000', 'blue': '#0000ff', 'black': '#000000', 'yellow': '#ffff00'}
        color_obj = Color.objects.get(id = obj.color.id)
        return {'color_hex' : col_hex_dict[color_obj.color_name.lower()]}


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username= data['username']):
                raise serializers.ValidationError('username is taken')

        if data['email']:
            if User.objects.filter(email= data['email']):
                raise serializers.ValidationError('email is taken')

        return data

    def create(self, validated_data):
        print(f"====> validated datd {validated_data}")
        user = User.objects.create(username= validated_data['username'], email= validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data