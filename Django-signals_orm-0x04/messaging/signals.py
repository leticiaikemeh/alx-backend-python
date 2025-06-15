from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User


@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, **kwargs):
    if created:
        # Logic to handle the creation of a new message
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
        MessageHistory.objects.create(
            message=instance,
            action='created'
        )
        print(
            f"New message created: {instance.content} from {instance.sender} to {instance.receiver}")


@receiver(pre_save, sender=Message)
def message_pre_save(sender, instance, **kwargs):
    if instance.pk:
        # Logic to handle updates to an existing message
        original = Message.objects.get(pk=instance.pk)
        if original.content != instance.content:
            MessageHistory.objects.create(
                message=instance,
                edited_by=instance.sender,
            )
            print(f"Message updated: {original.content} to {instance.content}")
    else:
        # Logic for new messages (handled in post_save)
        pass


@receiver(post_delete, sender=User)
def message_post_delete(sender, instance, **kwargs):
    # Logic to handle the deletion of a message
    Message.objects.filter(sender=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(
        message__sender=instance).delete()
    print(
        f"User deleted: {instance.username}")
