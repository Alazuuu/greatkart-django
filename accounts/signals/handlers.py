from django.contrib.staticfiles.storage import staticfiles_storage
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Account, UserProfile


@receiver(post_save, sender=Account)
def create_userprofile_for_new_user(sender, **kwargs):
    image = staticfiles_storage.url('images/user-profile.png')
    if kwargs['created']:
        UserProfile.objects.create(
            user=kwargs['instance'], profile_picture='user-profile.png')
