# Discord Music Bot

This is a simple Discord music bot built using `discord.py`, `yt-dlp`, and `ffmpeg`. The bot can play music from YouTube and SoundCloud links, manage a song queue, and provide basic playback controls such as play, pause, resume, stop, and skip.


## Table of Contents

- [Installation](#installation)
  - [Clone the Repository](#1-clone-the-repository)
  - [Install Dependencies](#2-install-dependencies)
  - [Configure the Bot](#3-configure-the-bot)
  - [Run the Bot](#4-run-the-bot)
- [Docker Setup](#docker-setup)
  - [Build the Docker Image](#1-build-the-docker-image)
  - [Run the Docker Container](#2-run-the-docker-container)
- [Commands](#commands)
  - [Example Usage](#example-usage)
- [Supported provider](#supported-provider)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/discord-music-bot.git
cd discord-music-bot
```

### 2. Install Dependencies

Ensure you have Python 3.8 or later installed, then install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Install ffmpeg

### 3. Configure the Bot

Create a ``.env`` file in the root directory and add your bot token:

```bash
# .env
BOT_TOKEN = 'your-bot-token-here'
```

### 4. Run the Bot

After configuring the bot, you can start it with:

```bash
python bot.py
```

## Docker Setup

To run the bot inside a Docker container, follow these steps:

### Build the Docker Image
In the root directory of your project, build the Docker image using the Dockerfile:

```bash
docker build -t discord-music-bot .
```

### Run the Docker Container
Run the Docker container with your bot:

```bash
docker run -d --name discord-music-bot discord-music-bot
```

## Commands

The bot uses slash commands to interact. Here are the available commands:

- ``/play <url>``: Play a song or playlist from a [Supported provider](#supported-provider).
- ``/pause``: Pause the currently playing song.
- ``/resume``: Resume the paused song.
- ``/skip``: Skip the currently playing song.
- ``/stop``: Stop the music and clear the queue.

### Example usage

```bash
/play https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## Supported provider

| Provider   | Song   | Playlist |
|------------|:------:|:----------:|
| YouTube    | ✅    | ✅       |
| SoundCloud | ✅    | ✅       |
| Piped      | ✅    | ❌       |
