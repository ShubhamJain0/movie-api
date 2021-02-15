from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, generics, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
# Create your views here.


User = get_user_model()




class CreateUser(generics.CreateAPIView):
	"""Creates a user"""
	serializer_class = UserSerializer




class ManagingUser(generics.RetrieveUpdateAPIView):
	"""Retrieves and updates the authenticated user profile"""
	serializer_class = UserSerializer
	authentication_classes = (TokenAuthentication, )
	permission_classes = (IsAuthenticated, )

	def get_object(self):
		"""Retrieves the authenticated user"""
		return self.request.user








class MovieViewSet(viewsets.ReadOnlyModelViewSet):

	queryset = Movie.objects.all()
	serializer_class = MovieSerializer
	authentication_classes = (TokenAuthentication, )





	@action(detail=True, methods=['POST', 'GET'], permission_classes=[IsAuthenticated])
	def rate_movie(self, request, pk=None):


		
		movie = Movie.objects.get(id=pk)
		user = request.user

		try:
			rating_exist = Rating.objects.get(user=user.id, movie=movie.id)
		except:
			rating_exist = None

		if rating_exist:
			if request.method == 'POST':
				if 'stars' in request.data:
					stars = request.data['stars']
					rating = Rating.objects.get(user=user.id, movie=movie.id)
					rating.stars = stars
					rating.save()

					response = {'message':'Your rating has been updated!'}
					return Response(response, status=status.HTTP_200_OK)
				else:
					response = {'message':'Please provide a valid rating!'}
					return Response(response, status=status.HTTP_400_BAD_REQUEST)

			else:
				serializer = RatingSerializer(rating_exist, many=False)
				response = {'message':serializer.data}
				return Response(response, status=status.HTTP_200_OK)

		else:
			if request.method == 'POST':
				if 'stars' in request.data:
					stars = request.data['stars']
					Rating.objects.create(user=user, movie=movie, stars=stars)

					response = {'message':'Your rating has been submitted!'}
					return Response(response, status=status.HTTP_200_OK)
				else:
					response = {'message':'Please provide a valid rating!'}
					return Response(response, status=status.HTTP_400_BAD_REQUEST)

			else:
				serializer = RatingSerializer(rating_exist, many=False)
				response = {'message':"You haven't rated this movie yet!"}
				return Response(response, status=status.HTTP_200_OK)





			



class RatingViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.DestroyModelMixin):

	queryset = Rating.objects.all()
	serializer_class = RatingSerializer
	authentication_classes = (TokenAuthentication, )
	permission_classes = (IsAuthenticated, )


	def get_queryset(self):
		"""Returns objects to current authenticated user only"""
		assigned_only = self.request.query_params.get('assigned_only')
		queryset = self.queryset
		if assigned_only:
			queryset = queryset.filter(Rating__isnull=False)

		return queryset.filter(user=self.request.user)
	



	