from app import app
from flask import render_template, request
import json
from collections import OrderedDict
from .utils import SourceFile
from os import path


# TODO: add language as parameter, for now Ukrainian is default target language
@app.route('/')
@app.route('/index')
def index():
  segments = []

  with open(
          path.join(
            app.config.get("CONFIG")["i18n_path"],
            app.config.get("CONFIG")["source"]["lang"] + ".json"
          ),
          encoding='utf-8'
  ) as f:
    segments_original = json.load(f, object_pairs_hook=OrderedDict)

  with open(
          path.join(
            app.config.get("CONFIG")["i18n_path"],
            "ua.json"
          ),
          encoding='utf-8'
  ) as f:
    segments_translated = json.load(f, object_pairs_hook=OrderedDict)

  with open(
          path.join(
            app.config.get("CONFIG")["i18n_path"],
            app.config.get("CONFIG")["target"]["ua"]["whitelist"]
          ),
          encoding='utf-8'
  ) as f:
    whitelist = json.load(f)

  for k, v in segments_original.items():
    segments.append(
      {
        "key": k,
        "original": v,
        "translation": segments_translated[k] if k in segments_translated else None,
        "in_whitelist": k in whitelist
      }
    )

  return render_template("index.html",
                         segments=segments)


# TODO: add language as parameter, for now Ukrainian is default target language
@app.route("/report", methods=["POST"])
def change():
  content = request.json
  sf = SourceFile(
    path.join(
      app.config.get("CONFIG")["i18n_path"],
      content["lang"].lower() + ".json"
    ),
    content["lang"]
  )
  sf.update_key(content["key"], content["translation"])
  sf.save()

  print("Updated {lang}: \"{key}\": \"{value}\"".format( # use content["lang"]
    lang=content["lang"],
    key=content["key"],
    value=content["translation"].replace('\n', '\\n')))

  return "OK"
