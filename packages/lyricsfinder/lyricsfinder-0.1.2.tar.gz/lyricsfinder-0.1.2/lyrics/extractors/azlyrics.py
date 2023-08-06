"""Extractor for azlyrics.com."""

import logging
import re

from ..extractor import LyricsExtractor
from ..models.lyrics import Lyrics

log = logging.getLogger(__name__)


class AZLyrics(LyricsExtractor):
    """Class for extracting lyrics."""

    name = "AZLyrics"
    url = "https://www.azlyrics.com/"
    display_url = "azlyrics.com"

    @classmethod
    def extract_lyrics(cls, url_data):
        """Extract lyrics."""
        url_data.headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"}
        bs = url_data.bs

        center = bs.body.find("div", {"class": "col-xs-12 col-lg-8 text-center"})
        lyrics = center.find("div", {"class": None}).text

        lyrics = re.sub(r"<br>", " ", lyrics)
        lyrics = re.sub(r"<i?>\W*", "[", lyrics)
        lyrics = re.sub(r"\W*<\/i>", "]", lyrics)
        lyrics = re.sub(r"(?=)(\&quot\;)", "\"", lyrics)
        lyrics = re.sub(r"<\/div>", "", lyrics)

        title = center.find("h1").text.strip()[1:-8]

        return Lyrics(title, lyrics)
