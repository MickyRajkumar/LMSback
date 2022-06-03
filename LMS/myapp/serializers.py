from rest_framework import serializers
from . models import *

from rest_framework_simplejwt.serializers import TokenObtainSerializer

class EmailTokenObtainSerializer(TokenObtainSerializer):
    user_name = NewUser.email


class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data



class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

class bookserializer(serializers.ModelSerializer):

    class Meta:
        model = book
        fields = '__all__'
        # depth = 1



class borrowserializer(serializers.ModelSerializer):
    

    class Meta:
        model = borrow
        fields = '__all__'
        #depth = 1

    def to_representation(self, instance):
        rep = super(borrowserializer, self).to_representation(instance)
        rep['student'] = instance.student.user_name
        rep['book'] = instance.book.book_name
        return rep


class BookCategoryserializer(serializers.ModelSerializer):

    class Meta:
        model = BookCategory
        fields = '__all__'

class Commentserializer(serializers.ModelSerializer):
    # student = NewUserSerializer(many=False, read_only=True)
    # student = serializers.ReadOnlyField(source='NewUser')
    # student = serializers.StringRelatedField()
    class Meta:
        model = comment
        fields = ('id','comment','time','book','student')
        # depth = 1
        # exclude = []

    def to_representation(self, instance):
        rep = super(Commentserializer, self).to_representation(instance)
        rep['student'] = instance.student.user_name
        return rep

