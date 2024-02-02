from rest_framework import serializers
from django.contrib.auth import get_user_model

from article.serializers import ArticleSerializer

class UserSerializer(serializers.ModelSerializer):
	favorites = ArticleSerializer(read_only=True, many=True)

	class Meta:
		model = get_user_model()
		fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=100, min_length=6, required=True)
	email = serializers.CharField(max_length=80, required=True)
	first_name = serializers.CharField(max_length=80, required=True)
	last_name = serializers.CharField(max_length=80, required=True)

	class Meta:
		model = get_user_model()
		fields = ['email', 'username', 'password', 'first_name', 'last_name']

	def create(self, validated_data):
		user_password = validated_data.get('password', None)
		db_instance = self.Meta.model(**validated_data)
		db_instance.set_password(user_password)
		db_instance.save()
		return db_instance

class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=100, min_length=6, required=True)
    new_password = serializers.CharField(max_length=100, min_length=6, required=True)
    confirm_new_password = serializers.CharField(max_length=100, min_length=6, required=True)