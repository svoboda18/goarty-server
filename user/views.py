from article.models import Article
from user.models import User
from user.permissions import IsAdminUser
from .serializers import UserRegistrationSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

class UsersViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    queryset = User.objects

    def get_queryset(self):
        return self.queryset.all()

class UserRegistrationAPIView(APIView):
	serializer_class = UserRegistrationSerializer
	permission_classes = (AllowAny,)

	def post(self, request):
		try: 
			serializer = self.serializer_class(data=request.data)
			instance = None
			if serializer.is_valid(raise_exception=True):
				instance = serializer.save()
				if instance:
					data = serializer.data
					data.pop("password")
					return Response(data=data, status=status.HTTP_201_CREATED)
		except:
			if instance:
				instance.delete()
			raise

class UserViewAPI(APIView):
	def post(self, request):
		if (not 'favorite' in request.data):
			return Response({ 'favorite': f'field must not be empty'})
		pk = request.data.get('favorite')
		favorite = Article.objects.filter(id=pk).first()
		if (favorite is None):
			return Response({ 'detail': f'invalid article id {pk}'})
		request.user.favorites.add(favorite)
		return self.get(request)
	
	def patch(self, request):
		if (not 'favorite' in request.data):
			return Response({ 'favorite': f'field must not be empty'})
		pk = request.data.get('favorite')
		favorite = Article.objects.filter(id=pk).first()
		if (favorite is None):
			return Response({ 'detail': f'invalid article id {pk}'})
		request.user.favorites.remove(favorite)
		return self.get(request)

	def get(self, request):
		serializer = UserSerializer(instance=request.user)
		data = serializer.data
		data.pop('password')
		return Response(data=data, status=status.HTTP_200_OK)