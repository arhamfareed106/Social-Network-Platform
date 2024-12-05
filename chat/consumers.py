import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import ChatRoom, Message, UserStatus
import base64
import os
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.room_id = self.scope['url_route']['kwargs']['room_id']
            self.room_group_name = f'chat_{self.room_id}'
            self.user = self.scope['user']

            if not self.user.is_authenticated:
                logger.error(f"Unauthorized connection attempt to room {self.room_id}")
                await self.close()
                return

            # Verify user has access to this room
            if not await self.user_has_room_access():
                logger.error(f"User {self.user.username} attempted to access unauthorized room {self.room_id}")
                await self.close()
                return

            logger.info(f"User {self.user.username} connecting to room {self.room_id}")

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

            # Set user as online
            await self.set_user_online()

            # Notify room about user's online status
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_status',
                    'username': self.user.username,
                    'status': 'online'
                }
            )
            
            logger.info(f"User {self.user.username} successfully connected to room {self.room_id}")

        except Exception as e:
            logger.error(f"Error in connect for user {getattr(self, 'user', 'unknown')} in room {getattr(self, 'room_id', 'unknown')}: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            # Set user as offline
            await self.set_user_offline()

            # Notify room about user's offline status
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_status',
                    'username': self.user.username,
                    'status': 'offline'
                }
            )

            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

            logger.info(f"User {self.user.username} disconnected from room {self.room_id}")

        except Exception as e:
            logger.error(f"Error in disconnect for user {getattr(self, 'user', 'unknown')} in room {getattr(self, 'room_id', 'unknown')}: {str(e)}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type', 'message')

            if message_type == 'message':
                message = data['message']
                file_data = data.get('file')
                
                # Save message to database
                message_obj = await self.save_message(message, file_data)

                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': self.user.username,
                        'timestamp': message_obj.timestamp.isoformat(),
                        'message_id': message_obj.id,
                        'file_url': message_obj.file.url if message_obj.file else None
                    }
                )
            elif message_type == 'typing':
                is_typing = data['is_typing']
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'typing_status',
                        'username': self.user.username,
                        'is_typing': is_typing
                    }
                )
            elif message_type == 'read_receipt':
                message_id = data['message_id']
                await self.mark_message_as_read(message_id)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'read_receipt',
                        'username': self.user.username,
                        'message_id': message_id
                    }
                )
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")

    async def chat_message(self, event):
        try:
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'type': 'message',
                'message': event['message'],
                'username': event['username'],
                'timestamp': event['timestamp'],
                'message_id': event['message_id'],
                'file_url': event.get('file_url')
            }))
        except Exception as e:
            logger.error(f"Error sending chat message: {str(e)}")

    async def typing_status(self, event):
        try:
            # Send typing status to WebSocket
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'username': event['username'],
                'is_typing': event['is_typing']
            }))
        except Exception as e:
            logger.error(f"Error sending typing status: {str(e)}")

    async def user_status(self, event):
        try:
            # Send user status to WebSocket
            await self.send(text_data=json.dumps({
                'type': 'status',
                'username': event['username'],
                'status': event['status']
            }))
        except Exception as e:
            logger.error(f"Error sending user status: {str(e)}")

    async def read_receipt(self, event):
        try:
            # Send read receipt to WebSocket
            await self.send(text_data=json.dumps({
                'type': 'read_receipt',
                'username': event['username'],
                'message_id': event['message_id']
            }))
        except Exception as e:
            logger.error(f"Error sending read receipt: {str(e)}")

    @database_sync_to_async
    def save_message(self, message_content, file_data=None):
        try:
            room = ChatRoom.objects.get(id=self.room_id)
            message = Message(room=room, sender=self.user, content=message_content)
            
            if file_data:
                try:
                    # Handle file upload
                    file_name = file_data['name']
                    file_content = base64.b64decode(file_data['content'])
                    file_path = f'chat_files/{room.id}/{file_name}'
                    
                    # Ensure directory exists
                    os.makedirs(os.path.dirname(f'media/{file_path}'), exist_ok=True)
                    
                    # Save file
                    with open(f'media/{file_path}', 'wb') as f:
                        f.write(file_content)
                    
                    message.file = file_path
                except Exception as e:
                    logger.error(f"Error saving file: {str(e)}")
            
            message.save()
            return message
        except Exception as e:
            logger.error(f"Error saving message: {str(e)}")

    @database_sync_to_async
    def set_user_online(self):
        try:
            status, _ = UserStatus.objects.get_or_create(user=self.user)
            status.is_online = True
            status.last_seen = timezone.now()
            status.save()
        except Exception as e:
            logger.error(f"Error setting user online: {str(e)}")

    @database_sync_to_async
    def set_user_offline(self):
        try:
            status = UserStatus.objects.get(user=self.user)
            status.is_online = False
            status.last_seen = timezone.now()
            status.is_typing = None
            status.save()
        except UserStatus.DoesNotExist:
            pass
        except Exception as e:
            logger.error(f"Error setting user offline: {str(e)}")

    @database_sync_to_async
    def mark_message_as_read(self, message_id):
        try:
            message = Message.objects.get(id=message_id)
            message.read_by.add(self.user)
        except Message.DoesNotExist:
            pass
        except Exception as e:
            logger.error(f"Error marking message as read: {str(e)}")

    @database_sync_to_async
    def user_has_room_access(self):
        try:
            room = ChatRoom.objects.get(id=self.room_id)
            return self.user in room.participants.all()
        except ChatRoom.DoesNotExist:
            return False
        except Exception as e:
            logger.error(f"Error checking room access: {str(e)}")
