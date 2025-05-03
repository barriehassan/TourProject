from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, TouristProfile, AgentProfile, AdminProfile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'tourist':
            TouristProfile.objects.create(user=instance)
        elif instance.user_type == 'agent':
            AgentProfile.objects.create(user=instance)
        elif instance.user_type == 'admin':
            AdminProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 'tourist':
        instance.touristprofile.save()
    elif instance.user_type == 'agent':
        instance.agentprofile.save()
    elif instance.user_type == 'admin':
        instance.adminprofile.save()

