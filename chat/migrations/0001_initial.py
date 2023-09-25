# Generated by Django 4.2.5 on 2023-09-24 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_author', to=settings.AUTH_USER_MODEL)),
                ('parent_message', models.ForeignKey(blank=True, limit_choices_to={'parent_message': None}, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.chatrecord')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['author'], name='chat_chatre_author__2c86eb_idx'), models.Index(fields=['receiver'], name='chat_chatre_receive_78764a_idx'), models.Index(fields=['created_at'], name='chat_chatre_created_38de3d_idx')],
            },
        ),
    ]