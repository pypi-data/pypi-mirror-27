import asyncio


def async_every(seconds=0, minutes=0, hours=0):
    def every_decorator(func):
        async def inner_wrapper(*args, **kwargs):
            asyncio.get_event_loop().call_later(
                seconds + 60 * minutes + 3600 * hours,
                asyncio.ensure_future,
                async_every(seconds=seconds, minutes=minutes, hours=hours)(func)(*args, **kwargs)
            )
            return await func(*args, **kwargs)
        return inner_wrapper
    return every_decorator
