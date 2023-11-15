from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.permissions import IsAuthor
from users.serializers import UserSerializer, UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import status


class UsersListView(generics.ListAPIView):
    """Отображение листа пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UsersDetailView(generics.RetrieveAPIView):
    """Отображение отдельного пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UsersCreateView(generics.CreateAPIView):
    """Создание пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UsersUpdateView(generics.UpdateAPIView):
    """Обновление информаии пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthor]


class UsersDeleteView(generics.DestroyAPIView):
    """Удаление пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthor]


class UsersRegistrationView(generics.CreateAPIView):
    """Регистрация пользователя"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data)
