import discord

class Song():
    def __init__(self, base_url: str, playable_url: str|None, title: str|None, artist: str|None, duration: str|None, thumbnail: str|None, provider: str|None) -> None:
        self.base_url = base_url
        self.playable_url = playable_url
        self.title = title
        self.artist = artist
        self.duration = duration
        self.thumbnail = thumbnail
        self.provider = provider

    def updateInfo(self, info: dict) -> None:
        self.playable_url = info['url']
        self.title = info['title']
        self.artist = info['uploader']
        self.duration = info['duration']
        self.thumbnail = info['thumbnail']
        self.provider = info['extractor']

    def displaySong(self) -> discord.Embed:
        embed = discord.Embed(
            title="Now Playing",
            url=self.base_url,
            description=self.title,
            color=self.__getProviderColor()
        )
        embed.add_field(name="Duration", value=self.__formatDuration(), inline=True)
        embed.add_field(name="Artist", value=self.artist, inline=True)
        embed.set_thumbnail(url=self.thumbnail)
        return embed

    def __formatDuration(self) -> str:
        hours, remainder = divmod(self.duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'
        else:
            return f'{int(minutes):02}:{int(seconds):02}'

    def __getProviderColor(self) -> discord.Color:
        return {
            'youtube': discord.Color.red(),
            'soundcloud': discord.Color.orange()
        }.get(self.provider, discord.Color.blue())
