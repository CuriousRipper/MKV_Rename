import json
import logging
import os
from trb.windows.dialogs import error_dialog, warning_dialog
from pathlib import Path
'''
    Tools for building ASIN, UPC, and text indexes of the databas
'''

def async_build_index(filename, basepath, notifier=None):
    if notifier is not None:
        notifier()


def build_index(filename, base_path):

    bundle = {"id": {'ASIN': {}, "UPC": {}},
              "keyword": {},
              "rel_path": ""
              }
    filetypes = ["imdb.json", "/metadata.json", "output.json", "release.json", "tmdb.json"]
    from datetime import datetime
    then = datetime.now()
    os.listdir()
    for series in os.listdir(base_path):
        series_path = base_path + "/" + series
        if os.path.isdir(base_path + "/" + series):
            for release in os.listdir(series_path):
                release_path = series_path + "/" + release
                if os.path.isdir(release_path):
                    for file in os.listdir(release_path):
                        if file in filetypes:
                            bundle["rel_path"] = series + "/" + release
                            _parse_release_file(release_path + "/" + file, bundle)

    try:
        with open(filename, 'w') as fptr:
            json.dump(bundle["id"], fptr)
    except:
       logging.error("Error saving index file")


    logging.info("Index build time: " + str(datetime.now() - then))

def _ensure_path(filename):
    output_file = Path(filename)
    output_file.parent.mkdir(exist_ok=True, parents=True)

def _parse_release_file(filename, data_bundle):
    try:
        with open(filename) as fptr:
            release = json.load(fptr)
            for key in release.keys():
                if key.lower() == "asin":
                    if release[key] in data_bundle["id"]["ASIN"]:
                        logging.warning("Duplicate ASIN: " + release[key] + ": " + filename)
                    data_bundle["id"]["ASIN"][release[key]] = data_bundle["rel_path"]

                if key.lower() == "upc":
                    if release[key] in data_bundle["id"]["UPC"]:
                        logging.warning("Duplicate UPC: " + release[key] + ": " + filename)
                    data_bundle["id"]["UPC"][release[key]] = data_bundle["rel_path"]
                # Eventually add keyword data
    except Exception as e:
        logging.warning("Error Indexing: " + filename + "\nError:" + str(e) )

def asin_search(asin, index_file, db_path=""):
    return id_search(asin, "ASIN", index_file, db_path)


def upc_search(upc, index_file, db_path=""):
    return id_search(upc, "UPC", index_file, db_path)


def index_refresh_check(index_file, db_path):
    """
    Check if the date modified on the series folder is newer than the index file and recommend rebuilding
    Not implemented
    :return:
    """
    pass

def id_search(identifier, id_type, index_file, db_path=""):
    """
    Search the index for the movie or series using the provide ASIN or UPC
    :param identifier: the ASIN or UPC being searched for
    :param id_type: ASIN | UPC
    :param index_file: relative path to the index file e.g. indices/series.json
    :param db_path: the path to the DiscDB data including the type of disc e.g. /home/.../data/series
    :return: path to the found release or an empty string
    """
    if db_path:
        index_refresh_check(index_file, db_path)

    try:
        with open(index_file) as fptr:
            db = json.load(fptr)[id_type]
            if identifier in db.keys():
                return db[identifier]
            else:
                msg = "The " + id_type + " was not found. Try updating your DB or add this release to it."
                warning_dialog(msg, "Not Found :'(")

    except:
        logging.error("Unable to load index file! Try rebuilding it?")
        error_dialog("Unable to load index file! Try rebuilding it?")

    return {}




# class ReleaseSearch