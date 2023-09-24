from rest_framework import status
from rest_framework.generics import (CreateAPIView, GenericAPIView, UpdateAPIView, RetrieveAPIView)
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Users
from .serializers import (UserRegistrationSerializer, UserLoginSerializer, UserUpdateSerializer)
from rest_framework.permissions import (AllowAny, IsAuthenticated)
import json
from .helper import calculate_similarity


class UserRegistrationView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Users.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = {
            'message': 'User registration successful',
            'user_data': serializer.data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class UserLoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create or retrieve an authentication token for the user
        access_token = serializer.validated_data.get('access_token')

        if access_token:
            return Response(
                {'message': 'Login successful', 'access_token': access_token},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'Login failed or something went wrong!', 'access_token': None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserUpdateView(UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'User data updated successfully', 'data': serializer.data},
            status=status.HTTP_200_OK
        )


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_obj = request.user
        if user_obj:
            user_obj.is_online = False
            user_obj.save()
            return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


class SuggestedFriendsView(RetrieveAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        user_id = kwargs['user_id']

        with open('users.json', 'r') as file:
            data = json.load(file)

        suggested_friends = []

        target_user = data["users"][user_id-1]
        target_interests = set(target_user["interests"])

        for user in data["users"]:
            if user != target_user:
                user_interests = set(user["interests"])
                if user_interests >= target_interests or user_interests <= target_interests:
                    similarity_score = calculate_similarity(target_user, user)
                    suggested_friends.append({"user": user, "similarity": similarity_score})

        suggested_friends.sort(key=lambda x: x["similarity"], reverse=True)

        return Response(
            {"message": 'Found recommendations!', "recommended_friends": suggested_friends[:5]},
            status=status.HTTP_200_OK
        )