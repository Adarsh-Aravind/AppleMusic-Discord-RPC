import asyncio
import winsdk.windows.media.control as wmc
from pypresence import AioPresence
import sys
import datetime
import os
from itunes_search import get_album_art

try:
    from secrets import CLIENT_ID
except ImportError:
    print("ERROR: secrets.py not found!", flush=True)
    print("Please rename secrets_example.py to secrets.py and add your Client ID.", flush=True)
    sys.exit(1)

class AppleMusicRPC:
    def __init__(self):
        self.rpc = None
        self.manager = None
        self.current_session = None
        self.last_track = None
        self.last_status = None

    def truncate(self, text, limit=127):
        if not text:
            return ""
        return text[:limit] + "..." if len(text) > limit else text
        
    async def connect_rpc(self):
        if self.rpc:
            return
            
        try:
            self.rpc = AioPresence(CLIENT_ID)
            # Add timeout to ensure we don't hang forever
            await asyncio.wait_for(self.rpc.connect(), timeout=10)
            print("Connected to Discord RPC")
        except Exception as e:
            print(f"Failed to connect to Discord RPC: {e}")
            self.rpc = None

    async def get_media_manager(self):
        # Retry loop to get the manager (sometimes fails on startup)
        while not self.manager:
            try:
                self.manager = await wmc.GlobalSystemMediaTransportControlsSessionManager.request_async()
            except Exception as e:
                # print(f"Error getting media manager: {e}")
                await asyncio.sleep(5)
                
    def get_session(self):
        if not self.manager:
            return None
        
        current = self.manager.get_current_session()
        if current:
            # STRICT FILTERING
            # We only want Apple Music. The AppUserModelId usually contains "AppleMusic" or "iTunes"
            app_id = current.source_app_user_model_id
            if app_id and ("AppleMusic" in app_id or "iTunes" in app_id):
                return current
            
            # Debug print to see what else is playing (e.g. Chrome, Spotify) to verify strictness
            # print(f"Checking session from: {app_id}")
            if app_id and ("AppleMusic" in app_id or "iTunes" in app_id):
                return current
            
            # print(f"Ignoring session: {app_id}")

    async def update_loop(self):
        while True:
            try:
                if not self.manager:
                    await self.get_media_manager()
                
                session = self.get_session()
                
                if session:
                    info = await session.try_get_media_properties_async()
                    playback_info = session.get_playback_info()
                    status = playback_info.playback_status
                    timeline = session.get_timeline_properties()
                    
                    if status == wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus.PLAYING:
                        title = info.title
                        artist = info.artist
                        album = info.album_title
                        album_artist = info.album_artist
                        
                        display_artist = artist if artist else album_artist
                        
                        # Timeline logic
                        start_time = None
                        end_time = None
                        
                        if timeline:
                            # Start and End times are in DateTime format if available
                            # Position is a TimeSpan
                            # We can calculate end timestamp for Discord using current time + remaining duration
                            # Remaining = End - Position
                            
                            # However, Windows Media Timeline properties can be tricky.
                            # Best way for Discord "Time Left" is: start_timestamp = now - position, end_timestamp = start + duration
                            
                            try:
                                # Convert TimeSpan to seconds
                                position_secs = timeline.position.total_seconds()
                                end_secs = timeline.end_time.total_seconds()
                                
                                if end_secs > 0:
                                    now = datetime.datetime.now().timestamp()
                                    start_time = int(now - position_secs)
                                    end_time = int(start_time + end_secs)
                            except Exception as e:
                                print(f"Timeline error: {e}", flush=True)
                                pass

                        # Create unique track signature to avoid redundant updates including cover art
                        # We include 'status' to force update on pause/play
                        track_sig = (title, display_artist, album, status)
                        
                        if track_sig != self.last_track:
                            print(f"Now Playing: {title} - {display_artist}")
                            
                            # Fetch Art asynchronously
                            cover_url = await get_album_art(display_artist, album, title)
                            
                            if not self.rpc:
                                await self.connect_rpc()

                            if self.rpc:
                                try:
                                    print("Sending RPC update...", flush=True)
                                    await self.rpc.update(
                                        details=self.truncate(title),
                                        state=self.truncate(f"by {display_artist}"),
                                        large_image=cover_url,
                                        large_text=self.truncate(album if album else "Apple Music"),
                                        small_image="playing",
                                        small_text="Playing",
                                        start=start_time,
                                        end=end_time
                                    )
                                    print("RPC update sent successfully.", flush=True)
                                except Exception as e:
                                    print(f"RPC Update failed: {e}", flush=True)
                                    self.rpc = None 

                            self.last_track = track_sig
                    
                    elif status == wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus.PAUSED:
                         if self.last_status != status:
                            print("Paused")
                            if self.rpc:
                                try:
                                    await self.rpc.clear()
                                except:
                                    pass
                            self.last_track = None 
                
                    self.last_status = status
                    
                else:
                    # No active Apple Music session
                    if self.last_status != "Stopped":
                        print("No active Apple Music session")
                        if self.rpc:
                            try:
                                await self.rpc.clear()
                            except:
                                pass
                        self.last_status = "Stopped"
                        self.last_track = None

                await asyncio.sleep(3) 

            except Exception as e:
                print(f"Error in loop: {e}")
                await asyncio.sleep(5)

    async def run(self):
        print("AppleMusicRPC.run called...", flush=True)
        await self.update_loop()

if __name__ == "__main__":
    # Ensure CLIENT_ID is set
    with open("rpc.pid", "w") as f:
        f.write(str(os.getpid()))
    print("Starting main...", flush=True)
    if CLIENT_ID == "YOUR_DISCORD_CLIENT_ID_HERE":
        print("ERROR: You must set the CLIENT_ID in main.py first!")
        input("Press Enter to exit...")
        sys.exit(1)
        
    # Reverting to manual loop handling for better compatibility with winsdk/pypresence on Windows
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = AppleMusicRPC()
    try:
        loop.run_until_complete(app.run())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
