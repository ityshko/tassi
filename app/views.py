from app import app
from flask import render_template, request
import json
from collections import OrderedDict
from .utils import SourceFile


@app.route('/')
@app.route('/index')
def index():
  segments = []

  with open(app.config.get("FILE_ORIG"), encoding='utf-8') as f:
    segments_original = json.load(f, object_pairs_hook=OrderedDict)

  with open(app.config.get("FILE_TRANS"), encoding='utf-8') as f:
    segments_translated = json.load(f, object_pairs_hook=OrderedDict)

  for k, v in segments_original.items():
    segments.append(
      {
        "key": k,
        "original": v,
        "translation": segments_translated[k] if k in segments_translated else None
      }
    )

  return render_template("index.html",
                         segments=segments)


@app.route("/report", methods=["POST"])
def change():
  content = request.json
  sf = SourceFile(app.config.get("FILE_TRANS"), "UA")
  sf.update_key(content["key"], content["translation"])
  sf.save()

  return "OK"
