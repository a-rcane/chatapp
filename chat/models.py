from user.models import Users
from django.db import models


class ChatBaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ChatRecord(ChatBaseModel):

    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="message_author")
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="message_receiver")
    message = models.TextField(blank=False, null=False)
    parent_message = models.ForeignKey(
        "self", on_delete=models.CASCADE, limit_choices_to={'parent_message': None}, null=True, blank=True
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Sent By: {self.author.username} - Received By: {self.receiver.username}'

    class Meta:
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['receiver']),
            models.Index(fields=['created_at']),
        ]
