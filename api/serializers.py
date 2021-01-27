from rest_framework import serializers
from .models import Movie, Rating
from django.contrib.auth import get_user_model



User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
	"""Takes in the user input"""

	class Meta:
		model = User
		fields = ('email', 'password', 'name')
		extra_kwargs = {'password':{'write_only':True, 'required':True}}

	def create(self, validated_data):
		"""Creates an object"""
		return User.objects.create_user(**validated_data)

	def update(self, instance, validated_data):
		"""Updates the user, sets password and returns user"""
		password = validated_data.pop('password', None)
		user = super().update(instance, validated_data)

		if password:
			user.set_password(password)
			user.save()

		return user




class RatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Rating
		fields = ('id', 'stars', 'movie', 'user')




class MovieSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movie
		fields = ('id', 'title', 'description')



class MovieDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movie
		fields = ('title', 'description', 'no_of_ratings', 'avg_ratings')

