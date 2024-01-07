from user.models import User
from user.permissions import IsAdminUser, IsModUser
from .serializers import UserRegistrationSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

class UserModViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    queryset = User.objects

    def get_queryset(self):
        return self.queryset.all().filter(is_staff=True, is_admin=False)

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
					return Response(serializer.data, status=status.HTTP_201_CREATED)
		except:
			if instance:
				instance.delete()
			raise

class UserViewAPI(APIView):
	def get(self, request):
		ser = UserRegistrationSerializer(instance=request.user)
		return Response(ser.data)