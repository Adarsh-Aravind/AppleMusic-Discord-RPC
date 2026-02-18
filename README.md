# Apple Music Discord Rich Presence

A lightweight, efficient, and automatic Discord Rich Presence for Apple Music on Windows.

## Features
-   **Strict Detection**: Only detects Apple Music/iTunes (ignores Chrome, Spotify, etc.).
-   **Album Art**: Automatically fetches high-resolution covers from iTunes API.
-   **Timeline**: Shows elapsed track time.
-   **Optimization**: Uses < 1% CPU and ~60MB RAM.
-   **Stability**: Truncates long titles to prevent Discord errors.
-   **Auto-Start**: Includes scripts for easy startup and kill switch.

## Setup

1.  **Install Python**: Make sure you have Python 3.10+ installed.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Secrets**:
    -   Rename `secrets_example.py` to `secrets.py`.
    -   Open `secrets.py` and replace `YOUR_CLIENT_ID_HERE` with your Discord Application ID.
    -   *Note: `secrets.py` is ignored by git to protect your ID.*

## Usage

-   **Start**: Double-click `Start Apple Music RPC.bat`.
-   **Stop**: Double-click `Stop Apple Music RPC.bat`.

## Files
-   `main.py`: Core logic.
-   `itunes_search.py`: Album art fetcher.
-   `kill_switch.py`: Script to forcefully stop the process.
-   `monitor_resources.py`: Utility to check RAM/CPU usage.

## License
MIT
