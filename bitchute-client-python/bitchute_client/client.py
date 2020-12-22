import aiohttp
import asyncio
import json
from urllib.parse import urlparse

from fake_useragent import UserAgent

from .video import Video
from . import common

class Client:
  def __init__(self, session_id=None):
    # Use a fake browser user agent so that BitChute displays the same content
    # as it would to a regular browser
    headers = { 'User-Agent': UserAgent().chrome }
    cookies = { 'sessionid': session_id } if session_id else {}
    self.session = aiohttp.ClientSession(headers=headers, cookies=cookies)

  async def __aenter__(self):
    return self

  async def __aexit__(self, exc_type, exc, tb):
    await self.close()

  async def close(self):
    await self.session.close()

  async def login(self, username, password):
    data = {
      'username': username,
      'password': password,
    }
    headers = {
      'Referer': common.endpoint('/'), # to pass CSRF validation
    }

    # Hit the main page at bitchute.com/ first to get a valid CSRF token
    async with self.session.get(common.endpoint('/')) as response:
      common.check_response(response, f'make initial connection to {common.endpoint("")}')
      soup = common.to_soup(await response.text())
      data[common.CSRF_TOKEN_KEY] = common.get_csrf_token(soup)

    # Post the username and password along with the collected CSRF token
    async with self.session.post(common.endpoint('/accounts/login/'),
        data=data, headers=headers) as response:
      common.check_response(response, 'log in')

      text = await response.text()
      result = json.loads(text)

      if not common.did_succeed(result):
        raise RuntimeError('Failed to log in: ' + result['errors'][0][1])

  def get_session_id(self):
    cookies = self.session.cookie_jar.filter_cookies(common.endpoint('/'))
    return cookies['sessionid'].value \
        if 'sessionid' in cookies \
        else None

  def get_video(self, code):
    return video.Video(self.session, code)

  # Get basic data about the current user, scraped from the /profile/ endpoint
  async def get_current_user(self):
    async with self.session.get(common.endpoint('/profile/'), allow_redirects=False) as response:
      if response.status != 200:
        return None
      soup = common.to_soup(await response.text())
      return {
        'username': soup.select('div[class=dropdown] > ul > li')[1].find('a').text,
        'display_name': soup.select_one('h1[class=page-title]').text,
      }

  async def upload(self, video, title, description, cover=None,
      sensitivity=common.Sensitivity.Normal, publish_now=True):

    # Need to get a one-shot upload URL. The /myupload/ endpoint will redirect
    # to a page on one of the upload servers, such as upload01.bitchute.com
    async with self.session.get(common.endpoint('/myupload/'), allow_redirects=False) as response:
      common.check_response(response, 'get one-shot upload URL', code=302)

      upload_url = response.headers['Location']
      url_parts = urlparse(upload_url)
      upload_url_base = f'{url_parts.scheme}://{url_parts.netloc}'

      # The query string in the URL you get redirected to contains several
      # parameters (upload_code, cid, cdid) that must be passed to the
      # upload endpoints. Extract the parameters for later.
      query = {}
      for param in url_parts.query.split('&'):
        tmp = param.split('=')
        query[tmp[0]] = tmp[1]

      # Get the upload page (redirect target) and extract its CSRF token
      # in order to upload media
      async with self.session.get(upload_url) as response:
        common.check_response(response, f'get {upload_url}')

        soup = common.to_soup(await response.text())
        csrf_token = common.get_csrf_token(soup)

        headers_base = { 'Referer': upload_url } # to pass CSRF validation
        data_base = {                            # needed for each following POST request
          common.CSRF_TOKEN_KEY: csrf_token,
          'upload_code': query['upload_code'],
        }

        # Upload cover or video. The upload_type is always 'video' even for
        # the cover, it looks like BitChute tells which it is by the MIME type
        async def _upload_media(media):
          data = { 'upload_type': 'video' }
          data.update(data_base)
          formdata = aiohttp.FormData(data)
          formdata.add_field('file', media.data, filename=media.name,
              content_type=media.mime_type)

          async with self.session.post(upload_url_base + '/videos/upload/',
              data=formdata, headers=headers_base) as response:
            common.check_response(response, 'upload media')

        # NOTE: does not work if done asynchronously
        await _upload_media(video)
        if cover:
          await _upload_media(cover)

        # Upload video metadata
        data = {
          'upload_title': title,
          'upload_description': description,
        }
        data.update(data_base)

        async with self.session.post(upload_url_base + '/videos/uploadmeta/',
            data=data, headers=headers_base) as response:
          common.check_response(response, 'upload video metadata')

        # Finalize the upload
        data = {
          'sensitivity': sensitivity.value,
          'publish_now': publish_now,
          'cid': query['cid'],
          'cdid': query['cdid'],
        }
        data.update(data_base)

        async with self.session.post(upload_url_base + '/videos/finish_upload/',
            data=data, headers=headers_base) as response:
          common.check_response(response, 'finish upload')

        return Video(self.session, query['upload_code'])
