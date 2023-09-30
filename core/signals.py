import re
import bleach
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from core.models import Avowal, Comment
from cache.redis import get_cache_key, set_cache_instance, delete_cache_instance


@receiver(pre_save, sender=Avowal)
def pre_save_avowal(sender, instance, **kwargs):
    body_clean = bleach.clean(instance.body, strip=True)
    instance.body = re.sub(r"http\S+", "", body_clean)


@receiver(post_save, sender=Avowal)
def post_save_avowal(sender, instance, created, **kwargs):
    pk = instance.id
    cache_key = get_cache_key(pk)
    if created:
        instance.public_identifier = instance.public_identifier_encode(pk=instance.id)
        instance.save()

        to_cache = instance.__class__.objects.with_comments(pk)

        set_cache_instance(cache_key, to_cache, 60)
    if not instance.is_active:
        delete_cache_instance(cache_key)


@receiver(pre_save, sender=Comment)
def pre_save_comment(sender, instance, **kwargs):
    body_clean = bleach.clean(instance.body, strip=True)
    instance.body = re.sub(r"http\S+", "", body_clean)


@receiver(post_save, sender=Comment)
def post_save_comment(sender, instance, created, **kwargs):
    if created:
        instance.public_identifier = instance.public_identifier_encode(pk=instance.id)
        instance.save()

        pk_avowal = instance.avowal_id
        cache_key = get_cache_key(pk_avowal)

        to_cache = instance.avowal.__class__.objects.with_comments(pk_avowal)

        delete_cache_instance(cache_key)
        set_cache_instance(cache_key, to_cache, 60)
