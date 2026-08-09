# 🎵 Day 46 — Musical Time Machine

## Course
**Python Programming Pro Bootcamp**

## Project

This is a free version of the Musical Time Machine project.

The program asks for a date, scrapes Billboard's Hot 100 chart using
**Requests + BeautifulSoup**, and saves the song titles with Spotify
search links into `songs.txt`.

> Spotify playlist creation requires Spotify Web API access. Since that
> requires Premium for current Development Mode access, this version
> uses Spotify search links instead.

## Technologies

- Python
- Requests
- BeautifulSoup
- Datetime
- File Handling
- Spotify Search URLs

## How to Run

Install the packages:

```bash
pip install -r requirements.txt
```

Run the program:

```bash
python main.py
```

Enter a date:

```text
2010-08-09
```

The results will be saved automatically in:

```text
songs.txt
```

## Project Structure

```text
Day46/
├── main.py
├── songs.txt
├── requirements.txt
├── README.md
└── screenshots/
    └── day46_output.png
```

## Screenshot

<!-- Add your screenshot here -->
<img width="1179" height="697" alt="image" src="https://github.com/user-attachments/assets/cad5e659-04b3-4b41-a28d-9f6e5d3ffd0b" />


## What I Learned

- Web scraping with BeautifulSoup
- Sending HTTP requests
- Parsing HTML
- Working with dates using `datetime`
- Extracting data from websites
- Writing data to text files
- Creating Spotify search URLs
- Automating repetitive tasks with Python

## 100 Days of Code

**Day 46 / 100** 🐍🎵
