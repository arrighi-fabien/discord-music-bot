import yt_dlp
import asyncio
import discord
from discord.ext import commands
from config import *
from utils.song import *
from utils.queue_manager import *

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

queue = QueueManager()

async def processSongs(url: str):
    with yt_dlp.YoutubeDL(YTDL_FORMAT_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)

        entries = info.get('entries', [info])
        for entry in entries:

            print(entry)
            # YouTube and SoundCloud song
            if 'id' in entry and entry.get('extractor', '') in SUPPORTED_PROVIDERS:
                song = Song(entry['webpage_url'], entry['url'], entry['title'], entry['uploader'], entry['duration'], entry['thumbnail'], entry['extractor'])
            # YouTube and SoundCloud playlist
            elif 'id' in entry and entry.get('ie_key', '').lower() in SUPPORTED_PROVIDERS:
                song = Song(entry['url'], None, None, None, None, None, None)
            else:
                continue

            await queue.addSong(song)

@tree.command(name='play', description='To play a song or playlist from a YouTube or SoundCloud URL')
async def play(interaction: discord.Interaction, url: str):
    voice_client = interaction.guild.voice_client

    if voice_client is None:
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            await channel.connect()
            voice_client = interaction.guild.voice_client
        else:
            await interaction.response.send_message("🔇 You are not connected to a voice channel.")
            return

    await interaction.response.send_message("🔄 Searching for your song...")

    async with interaction.channel.typing():
        await processSongs(url)

        if not voice_client.is_playing():
            await playNext(interaction)
        else:
            await interaction.followup.send(content="✅ Added to queue")

async def playNext(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if not queue.isEmpty():
        song = await queue.getNextSong()

        if song.playable_url == None:
            with yt_dlp.YoutubeDL(YTDL_FORMAT_OPTIONS) as ydl:
                info = ydl.extract_info(song.base_url, download=False)
                song.updateInfo(info)

        def afterPlaying(error):
            asyncio.run_coroutine_threadsafe(playNext(interaction), bot.loop)

        voice_client.play(discord.FFmpegPCMAudio(song.playable_url, **FFMPEG_OPTIONS), after=afterPlaying)
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
        voice_client.source.volume = float(100) / 100.0

        await interaction.channel.send(embed=song.displaySong())
    else:
        if voice_client.is_connected():
            await interaction.channel.send("🕳️ Queue is empty. Disconnecting.")
            await voice_client.disconnect()

@tree.command(name='pause', description='This command pauses the song')
async def pause(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
        await interaction.response.send_message("⏸️ Paused the song.")
    else:
        await interaction.response.send_message("🚫 Currently no audio is playing.")

@tree.command(name='resume', description='Resumes the song')
async def resume(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
        await interaction.response.send_message("▶️ Resumed the song.")
    else:
        await interaction.response.send_message("🚫 The audio is not paused.")

@tree.command(name='stop', description='Stops the song')
async def stop(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client.is_playing():
        await voice_client.disconnect()
        await queue.clearQueue()
        await interaction.response.send_message("⏹️ Stopped the song and cleared the queue.")
    else:
        await interaction.response.send_message("🚫 Currently no audio is playing.")

@tree.command(name='skip', description='Skips the current song')
async def skip(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await interaction.response.send_message("⏭️ Skipped the current song.")
    else:
        await interaction.response.send_message("🚫 Currently no audio is playing.")

@bot.event
async def on_ready():
    await tree.sync()
    print(f'We have logged in as {bot.user}')

bot.run(BOT_TOKEN)
