import aiohttp
import asyncio
from datetime import datetime, timezone
import json
import re

from . import common

VIDEO_TIME_REGEX = re.compile(
    r'First published at (\d\d:\d\d) (UTC) on ([A-Za-z]+) (\d+).., (\d+)\.')
def _convert_video_time(s):
  match = VIDEO_TIME_REGEX.match(s.strip())
  return datetime.strptime(' '.join(match.groups()), '%H:%M %Z %B %d %Y') \
      if match else datetime.fromtimestamp(0)

class Video:
  def __init__(self, session, code):
    self.session = session
    self.code = code
    self.url = common.endpoint(f'/video/{self.code}/')
    self._csrf_token = None

  async def __aenter__(self):
    await self.load()
    return self

  async def __aexit__(self, exc_type, exc, tb):
    pass

  async def get_counts(self):
    async with self.session.get(self.url + 'counts/') as response:
      result = json.loads(await response.text())
      return {} if not common.did_succeed(result) \
          else { key[:-6]+'s': value \
                 for key, value in result.items() \
                 if key.endswith('_count') }

  async def load(self):
    async with self.session.get(self.url) as response:
      common.check_response(response, f'load video page')
      soup = common.to_soup(await response.text())
      self._csrf_token = common.get_csrf_token(soup)

      self.title = soup.select_one('h1[id=video-title]').text
      self.description = soup.select_one('div[class=teaser]').text
      self.cover_url = soup.select_one('video[id=player]').get('poster')
      self.publish_date = _convert_video_time(
          soup.select_one('div[class=video-publish-date]').text)
      self.magnet_link = soup.select_one('a[href*=magnet]').get('href')
      self.hashtags = { a.text[1:]: a.get('href')[9:-1] \
                        for a in soup.select('span[id=video-hashtags] > ul > li > a') }

      self.channel = soup.select_one('div[class=details] > p[class=name] > a') \
          .get('href').split('/')[-2]
      self.profile = soup.select_one('div[class=details] > p[class=owner] > a') \
          .get('href').split('/')[-2]

      details = soup.select('table[class=video-detail-list] > tbody > tr > td > a')
      self.category = common.Category[details[0].text.replace(' & ', '_and_')]
      self.sensitivity = common.Sensitivity[details[1].text.split(' ')[0]]

      self.discussion_allowed = not soup.select('div[class=video-no-discussion]')

  async def save(self):
    if not self._csrf_token:
      self.load()

    data = {
      common.CSRF_TOKEN_KEY: self._csrf_token,
      'title': self.title,
      'description': self.description,
      'hashtags': ','.join(self.hashtags),
      'category': self.category.value,
      'sensitivity': self.sensitivity.value,
    }
    if self.discussion_allowed:
      data['is_discussable'] = 'on' # not present = off

    headers = {
      'Referer': self.url,
    }

    async with self.session.post(self.url + 'save/', data=data, headers=headers) as response:
      await common.check_response_success(response, 'save video metadata')

  async def _state_action(self, action):
    data = {
      common.CSRF_TOKEN_KEY: self._csrf_token,
      'action': action,
    }
    headers = {
      'Referer': self.url,
    }

    async with self.session.post(self.url + 'state/', data=data, headers=headers) as response:
      await common.check_response_success(response, action)

  async def publish(self):
    await self._state_action('publish')

  async def unpublish(self):
    await self._state_action('unpublish')

  async def delete(self):
    await self._state_action('delete')
