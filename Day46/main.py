import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote

# -----------------------------
# Ask the user for a date
# -----------------------------

date = input(
    "Which year do you want to travel to? "
    "Type the date in YYYY-MM-DD format: "
)

try:
    datetime.strptime(date, "%Y-%m-%d")
except ValueError:
    print("Invalid date format. Please use YYYY-MM-DD.")
    exit()

# -----------------------------
# Billboard Web Scraping
# -----------------------------

url = f"https://www.billboard.com/charts/hot-100/{date}/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("\nSearching Billboard...")

response = requests.get(url, headers=headers, timeout=15)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Billboard's current chart pages commonly use this selector.
song_elements = soup.select("li.o-chart-results-list__item h3")

song_names = []

for song in song_elements:
    title = song.get_text(strip=True)

    if title and title not in song_names:
        song_names.append(title)

# Keep the first 100 songs.
song_names = song_names[:100]

if not song_names:
    print("No songs were found.")
    print("The Billboard page structure may have changed.")
    exit()

print(f"\nFound {len(song_names)} songs!")

# -----------------------------
# Save songs + Spotify searches
# -----------------------------

with open("songs.txt", "w", encoding="utf-8") as file:

    for number, song in enumerate(song_names, start=1):
        spotify_search = (
            "https://open.spotify.com/search/"
            + quote(song)
        )

        file.write(f"{number}. {song}\n")
        file.write(f"Spotify Search: {spotify_search}\n\n")

print("\nSongs have been saved to songs.txt")
print("Musical Time Machine completed successfully! 🎵")
