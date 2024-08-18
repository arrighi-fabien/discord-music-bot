from asyncio import Queue
from utils.song import Song

class QueueManager():
    def __init__(self) -> None:
        self.queue = Queue()

    async def addSong(self, song: Song) -> None:
        await self.queue.put(song)

    async def getNextSong(self) -> Song | None:
        if not self.queue.empty():
            return await self.queue.get()
        return None

    def isEmpty(self) -> bool:
        return self.queue.empty()

    async def clearQueue(self) -> None:
        while not self.queue.empty():
            await self.queue.get()
