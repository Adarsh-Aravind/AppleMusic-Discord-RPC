# Apple Music Discord Rich Presence

Shows what you're playing in Apple Music (or iTunes) on Windows as your Discord status: track, artist, album art and a live progress bar. It runs quietly in the background and uses very little CPU or memory.

## Features

- **Apple Music only:** reads the Windows media controls but ignores every other player (Spotify, browsers and so on), so your status never shows the wrong thing
- **Album art:** looks up the cover for each track through the iTunes Search API
- **Live timeline:** Discord shows elapsed and remaining time for the current song
- **Lightweight:** polls every few seconds, typically under 1% CPU and around 60 MB of RAM
- **Safe with long titles:** titles and artist names are trimmed to fit Discord's limits
- **Recovers on its own:** reconnects to Discord and to the Windows media session if either drops
- **Background mode and autostart:** start it without a console window, stop it with one click, or add it to Windows startup

## Requirements

- Windows 10 or 11
- Python 3.10+
- The Discord desktop app
- A Discord application (free) from the [Discord Developer Portal](https://discord.com/developers/applications). Its name is what appears as "Listening to …" on your profile.

## Setup

```bash
git clone https://github.com/Adarsh-Aravind/AppleMusic-Discord-RPC.git
cd AppleMusic-Discord-RPC
pip install -r requirements.txt
```

1. Rename `secrets_example.py` to `secrets.py`.
2. Replace `YOUR_CLIENT_ID_HERE` with your Discord application's ID. `secrets.py` is git-ignored.
3. Optional: in your Discord application, go to **Rich Presence → Art Assets** and upload an image named `playing`. It's shown as the small icon next to the album art.

## Usage

| Script | What it does |
| ------ | ------------ |
| `Start Apple Music RPC.bat` | Starts the presence in the background (no console window) |
| `Stop Apple Music RPC.bat` | Stops any running instance |
| `Debug Apple Music RPC.bat` | Stops background instances and runs in a console so you can see "Now Playing" logs |
| `python autostart.py` | Adds the app to Windows startup for your user account |

To remove it from startup, delete the `AppleMusicRPC` entry under `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`, or disable it in Task Manager's **Startup apps**.

## How it works

1. `main.py` asks Windows for the current media session (`GlobalSystemMediaTransportControlsSessionManager`, via `winsdk`).
2. If the session belongs to Apple Music or iTunes, it reads the title, artist, album and timeline.
3. When the track changes, `itunes_search.py` fetches the album cover URL.
4. The presence is sent to the Discord desktop app over local IPC with `pypresence`. When playback pauses or stops, the status is cleared.

## Project structure

| File | Purpose |
| ---- | ------- |
| `main.py` | Media session polling and Discord presence updates |
| `itunes_search.py` | Album art lookup via the iTunes Search API |
| `kill_switch.py` | Finds and stops running instances |
| `autostart.py` | Registers the app to start with Windows |
| `secrets_example.py` | Template for your Discord client ID |

## License

MIT
