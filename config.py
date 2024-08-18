from decouple import config

BOT_TOKEN = config('BOT_TOKEN')
YTDL_FORMAT_OPTIONS = {
    'format': 'bestaudio/best',
    'extract_flat': True
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}
SUPPORTED_PROVIDERS = {
    'youtube',
    'soundcloud'
}
