from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class CustomUserModelManager(BaseUserManager):

	def create_user(self, email, password=None, **extra_fields):

		if not email:
			raise ValueError('Email is needed!')

		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)

		return user


	def create_superuser(self, email, password):

		user = self.create_user(email, password)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)

		return user








class CustomUserModel(AbstractBaseUser, PermissionsMixin):

	email = models.EmailField(unique=True, max_length=255)
	name = models.CharField(null=True, max_length=255)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = CustomUserModelManager()

	USERNAME_FIELD = 'email'








class Movie(models.Model):

	title = models.CharField(max_length=30)
	description = models.TextField(max_length=300)

	def __str__(self):

		return self.title

	def no_of_ratings(self):
		ratings = Rating.objects.filter(movie=self)
		return len(ratings)

	def avg_ratings(self):
		ratings = Rating.objects.filter(movie=self)
		sum = 0
		for rating in ratings:
			sum += rating.stars

		if len(ratings) > 0:
			return sum / len(ratings)
		else:
			return 0


class Rating(models.Model):

	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

	class Meta:

		unique_together = (('user', 'movie'),)
		index_together = (('user', 'movie'),)







