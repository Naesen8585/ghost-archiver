# A BitChute Client for Python 3

This is BitChute client library, written in Python 3 with `aiohttp` for
asynchronous I/O. Because BitChute has no public API, it operates using a hacky
combination of reverse-engineered API calls and data scraped from the site's
user-visible pages. Calls made with this library will be faster than using
BitChute in your browser, but still slower than they could be with a dedicated
API, because the client still has to download and parse whole web pages to get
the data it needs.

This library is in early alpha. It currently only supports logging in and
uploading videos, so it can be used to perform batch uploads to BitChute
(useful for restoring videos archived from YouTube), but not much else.

I am planning to add more features, such as search, notifications and account
settings. Unfortunately my ability to do so is limited because BitChute does
not have a public API.

## Usage example

Below is an example of upload functionality.

```
import asyncio
import bitchute_client as bc

async def main():
  async with bc.Client() as client:
    await client.login('<username>', '<password>')
    await client.upload(
        bc.Media.from_file('/path/to/video.mp4'),
        cover=bc.Media.from_file('/path/to/cover.jpg'),
        title='Video Title', description='Video description')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

If you are uploading a file on your computer, you will want to use
`Media.from_file()`, but you can also manually create a `Media` object
to do things like uploading data directly as you download it from somewhere
else, without saving to the filesystem in between. See `media.py` for details.

Once you log in, you can also get and save your session ID, then use it to
directly resume your session so you don't have to log in again, as long as
your session has not expired.

```
async with bc.Client() as client1:
  await client.login('<username>', '<password>')
  sid = client.get_session_id()
  # save sid...

# some time later...
async with bc.Client(session_id=sid) as client:
  await client.upload(...) # no need to log in
```
