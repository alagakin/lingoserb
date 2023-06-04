from django.core.cache import cache


def topic_progress_cache_key(topic_id: int, user_id: int) -> str:
    return f"learn_topic:{topic_id}:{user_id}"


def clear_topic_progress_cache(topic_id: int, user_id: int):
    cache_key = topic_progress_cache_key(topic_id, user_id)
    cache.delete(cache_key)
