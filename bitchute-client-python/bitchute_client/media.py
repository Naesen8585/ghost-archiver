import mimetypes
from pathlib import Path

class Media:
  @classmethod
  def from_file(self, path):
    p = Path(path)
    return Media(p.name, mimetypes.guess_type(p.name)[0], p.open('rb'))

  def __init__(self, name, mime_type, data):
    self.name = name
    self.mime_type = mime_type
    self.data = data
