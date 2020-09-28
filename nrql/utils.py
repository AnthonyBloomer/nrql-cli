from __future__ import unicode_literals

import json
import os
import platform
import sys
import time

from halo import Halo

from .api import NRQL

WORDS = "/tmp/words.json"


def creation_date(path_to_file):
    """
    Get the creation date of the file.
    :param path_to_file: str
    :return: str
    """
    if platform.system() == "Windows":
        return os.path.getctime(path_to_file)
    stat = os.stat(path_to_file)
    try:
        return stat.st_birthtime
    except AttributeError:
        return stat.st_mtime


def generate_word_list():
    """
    Generate word list.
    :return:
    """
    event_types_query = "show event types since 1 week ago"
    with Halo(text="Loading...", spinner="dots"):
        reserved_words = [
            "ago",
            "and",
            "as",
            "auto",
            "begin",
            "begintime",
            "compare",
            "day",
            "days",
            "end",
            "endtime",
            "explain",
            "facet",
            "from",
            "hour",
            "hours",
            "in",
            "is",
            "like",
            "limit",
            "minute",
            "minutes",
            "month",
            "months",
            "not",
            "null",
            "offset",
            "or",
            "second",
            "seconds",
            "select",
            "since",
            "timeseries",
            "until",
            "week",
            "weeks",
            "where",
            "with",
        ]
        nrql = NRQL()
        events = nrql.query(event_types_query)
        if "error" in events:
            sys.exit(events["error"])
        events = events["results"][0]["eventTypes"]
        words = list(set(reserved_words + events))
    return words


def load_or_generate():
    """
    Check if the word file exists.
    If it does read and decode JSON otherwise generate the word list and write to /tmp/words.json
    :return:
    """
    if not os.path.isfile(WORDS) or not os.path.getsize(WORDS):
        with open(WORDS, "w") as outfile:
            word_list = generate_word_list()
            json.dump({"words": word_list}, outfile)
            return word_list
    filename = creation_date(WORDS)
    timestamp_now = time.time()
    difference = abs(filename - timestamp_now) / 60 / 60 / 24
    if difference > 7:
        word_list = generate_word_list()
        with open(WORDS, "w") as outfile:
            json.dump({"words": word_list}, outfile)
        return word_list

    with open(WORDS) as filename:
        word_list = json.load(filename)
        return word_list["words"]
