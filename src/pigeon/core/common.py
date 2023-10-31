import asyncio


def sync_to_async(sync_func):
    """
    Turns a sync function into its async counterpart.
    """
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, sync_func, *args, **kwargs)
    return wrapper
