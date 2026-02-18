import aiohttp
import urllib.parse
import asyncio

async def get_album_art(artist, album, title):
    """
    Searches iTunes API for the track/album and returns the best quality artwork URL.
    """
    if not artist or not title:
        return None

    # Construct search query
    # Prioritize searching by "Title Artist" for better match
    query = f"{title} {artist}"
    encoded_query = urllib.parse.quote(query)
    url = f"https://itunes.apple.com/search?term={encoded_query}&media=music&entity=song&limit=1"

    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json(content_type=None)
                    results = data.get("results", [])
                    
                    if results:
                        # Get artwork URL (usually 100x100), modify to get higher res
                        artwork_url = results[0].get("artworkUrl100")
                        if artwork_url:
                            # Apple hosts typically allow replacing 100x100bb with 1024x1024bb
                            return artwork_url.replace("100x100bb", "1024x1024bb")
    except Exception as e:
        print(f"Error fetching album art: {e}")
    
    return "apple_music_logo" # Fallback to default asset key

if __name__ == "__main__":
    # Test
    async def test():
        print(await get_album_art("The Weeknd", "Starboy", "Starboy"))
    
    asyncio.run(test())
