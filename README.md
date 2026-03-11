# Apple Music Discord Rich Presence

A lightweight, efficient, and automated Discord Rich Presence integration for Apple Music on Windows.

## Overview

This application provides real-time status updates on Discord, displaying the currently playing track on Apple Music or iTunes. It is designed to be highly resource-efficient and strictly filters out other media applications to ensure accurate presence information.

## Features

- **Strict Detection**: Accurately identifies Apple Music and iTunes, ignoring other media players such as Chrome or Spotify.
- **Album Artwork**: Automatically retrieves high-resolution album covers using the iTunes API.
- **Playback Timeline**: Displays the elapsed and remaining time for the current track.
- **Optimized Performance**: Maintains a minimal resource footprint, utilizing less than 1% CPU and approximately 60MB RAM.
- **Enhanced Stability**: Automatically truncates excessively long track titles to prevent Discord API errors.
- **Process Management**: Includes batch scripts for convenient startup and process termination.

## Prerequisites

- Python 3.10 or higher installed on your system.
- An active Discord Application ID.

## Installation and Configuration

1. **Clone the repository** (or download the source code).
2. **Install the required dependencies** via `pip`:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure the application secrets**:
   - Rename the `secrets_example.py` file to `secrets.py`.
   - Open `secrets.py` and replace `YOUR_CLIENT_ID_HERE` with your actual Discord Application ID.
   - *Note: `secrets.py` is included in `.gitignore` to protect your sensitive credentials.*

## Usage

- **To start the application**: Double-click the `Start Apple Music RPC.bat` file.
- **To stop the application**: Double-click the `Stop Apple Music RPC.bat` file.

## Project Structure

- `main.py`: Contains the core application logic and Discord RPC integration.
- `itunes_search.py`: Handles the fetching of album artwork from the iTunes API.
- `kill_switch.py`: Provides the functionality to forcefully terminate the rich presence process.
- `monitor_resources.py`: A utility script for monitoring CPU and RAM usage.

## License

This project is licensed under the MIT License.
