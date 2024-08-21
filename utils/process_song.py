import yt_dlp
from utils.song import Song
from utils.queue_manager import QueueManager
from config import YTDL_FORMAT_OPTIONS, SUPPORTED_PROVIDERS

class ProcessSong:
    @staticmethod
    async def processSongs(url: str, queue: QueueManager = None, song: Song = None):
        with yt_dlp.YoutubeDL(YTDL_FORMAT_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)

            if song:
                song.updateInfo(info)
                return

            entries = info.get('entries', [info])
            for entry in entries:
                extractor = entry.get('extractor', '').lower()
                ie_key = entry.get('ie_key', '').lower()

                if extractor in SUPPORTED_PROVIDERS or ie_key in SUPPORTED_PROVIDERS:
                    song = Song(
                        entry.get('webpage_url', entry.get('url')),
                        entry.get('url') if not ie_key else None,
                        entry.get('title'),
                        entry.get('uploader'),
                        entry.get('duration'),
                        entry.get('thumbnail'),
                        extractor
                    )
                    if queue:
                        await queue.addSong(song)
