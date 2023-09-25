from channels.layers import get_channel_layer
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.serializers import OnlineUsersSerializer
from user.models import Users


class OnlineUsersView(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = OnlineUsersSerializer

    def get_queryset(self):
        return Users.objects.filter(is_online=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            'message': 'Online users fetched successfully',
            'data': serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class StartChatView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Users.objects.all()

    def post(self, request, *args, **kwargs):
        user = self.get_object()

        if user is None:
            return Response({'error': "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.is_online:
            channel_layer = get_channel_layer()
            channel_layer.send(
                user.private_channel_name,
                {
                    'type': 'chatroom.message',
                    'message': 'message',
                    'username': 'self.user_name',
                    'receiver_user_id': 'receiver_user_id',
                    'chat_type': 'private',
                    'sent_by': 'self.user_id'
                }
            )
            return Response({'message': 'Message sent !'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'User not online'}, status=status.HTTP_400_BAD_REQUEST)
