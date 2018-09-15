import json
from collections import OrderedDict


class SourceFile:

  def __init__(self, fpath, lang):
    with open(fpath, encoding='utf-8') as f:
      self.path = fpath
      self.lang = lang
      self.content = json.load(f, object_pairs_hook=OrderedDict)

  def update_key(self, k, v):
    if k in self.content:
      self.content[k] = v

  def save(self):
    with open(self.path, "w", encoding='utf-8') as f:
      json.dump(self.content, f, indent=2, ensure_ascii=False)

