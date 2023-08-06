"""
gidown.search
~~~~~~~~~~~~~
This module implements functions and classes for acquiring images from google image search.

:license: Apache2, see LICENSE for more details.
"""

import json
from imghdr import what
from typing import List
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from gidown.query import QueryBuilder
from gidown.advanced import QuerySettings, QuerySetting


class GoogleSearchImage:

    """
    Class used to store information about images from google image search. 
    Two **GoogleSearchImage** are considered the same if they have the same image URL.
    """

    def __init__(self, google_json_dict: dict):
        """
        
        
        :param google_json_dict: Dictionary as found in <div> for each image on google image search pages  
        """

        self.url = google_json_dict["ou"]
        self.tb_url = google_json_dict["tu"]

        self.src_url = google_json_dict["ru"]
        self.src_domain = google_json_dict["isu"]

        self.title = "pt"
        self.desc = "s"

        self.width = google_json_dict["ow"]
        self.height = google_json_dict["oh"]
        self.type = google_json_dict["ity"]

        self.tb_width = google_json_dict["tw"]
        self.tb_height = google_json_dict["th"]
        self.tb_type = google_json_dict["ity"]

        self.image = None
        self.thumbnail = None

    def __eq__(self, other):
        if not hasattr(other, "image_url"):
            return False
        return self.url == other.image_url

    def __hash__(self):
        return hash(self.url)

    def __str__(self):
        return "Downloadable {} at {}".format(self.type, self.url)

    def download(self, download_all=False, check_ext=True) -> None:
        """
        Download the image and store raw bytes into **self.image**.
        Image type (extension) is automatically detected from the raw bytes if possible (**type**).

        :param check_ext: Checks if extensions is correct. Raises ValueError if extension cannot be determined from image.
        :param download_all: Also download thumbnail and store it in **self.thumbnail**.
        """

        self.image = requests.get(self.url).content
        if download_all:
            self.download_thumbnail()
        ext = what(None, self.image)
        if check_ext and ext is None:
            raise ValueError("Unknown file format.")
        self.type = ext if ext is not None else self.type

    def download_thumbnail(self) -> None:
        """
        Download the thumbnail and store raw bytes into **self.thumbnail**.
        Image type (extension) is automatically detected from the raw bytes if possible (**thumbnail_type**).
        """
        self.thumbnail = requests.get(self.tb_url).content
        ext = what(None, self.image)
        self.tb_type = ext if ext is not None else self.tb_type

    @staticmethod
    def _save(img_data, filename):
        with open(filename, "wb") as fout:
            fout.write(img_data)

    def save(self, filename: str, auto_ext=False):
        """
        Save image to filesystem. If the image was not downloaded using **download** it is done now.
               
        Image type (extension) is automatically detected from the raw bytes if possible, otherwise the type is
        determined from the google image search dictionary.

        :param filename: Path to store the image to.
        :param auto_ext: Automatically add the file extension.
        """
        if self.image is None:
            self.download()

        if auto_ext:
            filename = "{}.{}".format(filename, self.type)
        self._save(self.image, filename)

    def save_thumbnail(self, filename, auto_ext=False):
        """
        Save thumbnail to filesystem. If the thumbnail was not downloaded using **download_thumbnail** it is done now.
               
        Image type (extension) is automatically detected from the raw bytes if possible, otherwise the type is
        determined from the google image search dictionary.

        :param filename: Path to store the thumbnail to.
        :param auto_ext: Automatically add the file extension.
        """
        if self.thumbnail is None:
            self.download_thumbnail()

        if auto_ext:
            filename = "{}.{}".format(filename, self.tb_type)
        self._save(self.thumbnail, filename)


_USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
_URL = "https://www.google.hr/search"


def _generate_url(query, settings, autocorrect=False):
    q = {"tbm": "isch",
         "tbs": QuerySettings(settings).urlencode(),
         "q": quote_plus(query.strip()),
         "source": "lnms"}
    if not autocorrect:
        q["nfpr"] = 1
    return "{}?{}".format(_URL, "&".join("{}={}".format(k, v) for k, v in q.items()))


def _fetch_html(url):
    req = requests.get(url, headers={'User-Agent': _USER_AGENT})
    html_doc = req.text
    return html_doc


def image_query(query: str or QueryBuilder, *restrictions: QuerySetting, autocorrect=False) -> List[GoogleSearchImage]:
    """
    Query google for images that satisfy all the restrictions.

    :param query: Query string, supports all advanced google search options.(see gis.query for wrappers around often used options) 
    :param restrictions: Variable amount of advanced search options. (see gis.advanced)
    :param autocorrect: Auto-correct queries that have a high likelihood of a misspell (e.q. "color grenn")
    :return: List of unique GoogleSearchImage objects that can be downloaded and saved.
    """
    url = _generate_url(query, restrictions, autocorrect)
    html = _fetch_html(url)

    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all("div", {"class": "rg_meta"})

    data = [json.loads(div.text) for div in divs]
    return list(set(GoogleSearchImage(img_data) for img_data in data))
