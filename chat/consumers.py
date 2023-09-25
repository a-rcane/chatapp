import json

from channels.generic.websocket import AsyncWebsocketConsumer

from chat.consumer_helper import save_user_channel_name, set_user_offline, get_user_channel_name, save_chat


class PersonalChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_id = None

    # connect user
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        await self.accept()
        await save_user_channel_name(user_id=self.user_id, channel_name=self.channel_name)

    # disconnect user
    async def disconnect(self, code):
        await set_user_offline(self.user_id)

    # send msg after validating user online status
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        receiver_user_id = text_data_json['send_to']

        send_to = await get_user_channel_name(user_id=text_data_json['send_to'])

        if send_to:
            await self.channel_layer.send(
                send_to,
                {
                    'type': 'chatroom.message',
                    'message': message,
                    'receiver_user_id': receiver_user_id,
                    'sender_id': self.user_id
                }
            )
        else:
            print("Consumer receive method error.")

    # send message over ws
    async def chatroom_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    'message': event['message'],
                    'sender_id': event['sender_id']
                }
            )
        )

        await save_chat(event)
