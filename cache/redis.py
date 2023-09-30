from django.core.cache import cache


def get_cache_key(pk=None):
    return f"avowal_object_{pk}"


def get_instance_from_cache(cache_key):
    return cache.get(cache_key)


def set_cache_instance(cache_key, instance, timeout):
    cache.set(cache_key, instance, timeout)


def delete_cache_instance(cache_key) -> bool:
    return cache.delete(cache_key)
