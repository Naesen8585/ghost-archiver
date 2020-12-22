import asyncio
from bs4 import BeautifulSoup
from enum import Enum
import json

BASE_URL = 'https://www.bitchute.com'
CSRF_TOKEN_KEY = 'csrfmiddlewaretoken'

class Sensitivity(Enum):
  Normal = 13
  NSFW = 15
  NSFL = 18

class Category(Enum):
  Unknown = -1
  Anime_and_Animation = 14
  Arts_and_Literature = 19
  Auto_and_Vehicles = 20
  Beauty_and_Fashion = 17
  Business_and_Finance = 3
  Cuisine = 13
  DIY_and_Gardening = 18
  Education = 6
  Entertainment = 12
  Gaming = 2
  Health_and_Medical = 4
  Music = 5
  News_and_Politics = 1
  Other = 11
  People_and_Family = 15
  Pets_and_Wildlife = 16
  Science_and_Technology = 7
  Spirituality_and_Faith = 9
  Sports_and_Fitness = 8
  Travel = 21
  Vlogging = 10

def did_succeed(result):
  return 'success' in result and result['success'] == True

def get_selected(tag):
  return tag.find('option', selected=True)

def get_tag_value_or_default(tag, default, name='value'):
  return tag.get(name) or default if tag else default

def endpoint(endpoint):
  return BASE_URL + endpoint

def to_soup(content):
  return BeautifulSoup(content, features='html5lib')

def get_csrf_token(soup):
    token_tag = soup.find('input', { 'name': 'csrfmiddlewaretoken' })
    return token_tag['value'] if token_tag else None

def check_response(response, what, code=200):
  if response.status != code:
    raise RuntimeError(f'Failed to {what}')

async def check_response_success(response, what, code=200):
  if response.status != code:
    raise RuntimeError(f'Failed to {what}')
  result = json.loads(await response.text())
  if not did_succeed(result):
    raise RuntimeError(f'Failed to {what}')
