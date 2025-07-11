import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

def fetch_data(movie_search):
  """
  Fetches movie information from API.
  Returns a dictionary with the requested movie information.
  """
  api_url = f'http://www.omdbapi.com/?t={movie_search}'
  response = requests.get(api_url, API_KEY)
  if response.status_code == requests.codes.ok:
    return response.json()
  else:
    raise Exception(f"API Error: {response.status_code} - {response.text}")
  
print(fetch_data("batman"))
