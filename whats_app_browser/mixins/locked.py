from asyncio.locks import Lock


class Locked:
    def __init__(self):
        self._lock = Lock()

    async def __aenter__(self):
        await self._lock.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()
