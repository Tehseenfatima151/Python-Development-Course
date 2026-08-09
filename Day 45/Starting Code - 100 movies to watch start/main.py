import requests
from bs4 import BeautifulSoup

URL = "https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")

movies = soup.find_all("h2")

movie_titles = []

for movie in movies:
    title = movie.get_text(strip=True)
    movie_titles.append(title)

# Reverse the list so movies are saved from 1 to 100
movie_titles.reverse()

with open("movies.txt", "w", encoding="utf-8") as file:
    for movie in movie_titles:
        file.write(movie + "\n")

print("100 Movies saved successfully! 🎬")