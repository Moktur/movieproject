# Welcome to my Movie App

This basic app let you create an own database. You can search for a movie by the menu, just press a number and follow the instructions of the CLI.

If you start from scratch, it is recommended to add some movies to your database first. They will get automatically added to you database by using the imddb API.

## What you need

python, some modules listet in requirements.txt and a internet connection.

## Functionality
- **adding movies** automaticaly adds movies from OMDB API with year, rating and poster.
- **SQLite database** 
- **Generation of static website** including movieposters

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd movie-database
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file with your API key:
```
API_KEY=your_api_key_here
```

4. For a fresh start delete movies.db otherwise you can the programm out with the already created db.