"""
gidown.advanced
~~~~~~~~~~~~~~~
This module contains advanced image search options.

:license: Apache2, see LICENSE for more details.
"""

import datetime
import re


class QuerySetting:

    """
    General class to represent a single advanced search option. 
    Generally shouldn't be used outside the scope of this file.
    """

    def __init__(self, setting_str: str):
        """       
        General class to represent a single advanced search option. 
        
        :param setting_str: String as it appears in tbs argument of google image search URL. Format: "key":"value"
        
        """

        if setting_str and not re.match("^.+:.+$", setting_str):
            raise ValueError("Setting string must be in the format <key>:<value>, {} was given".format(setting_str))
        self._setting = setting_str

    def __str__(self):
        return self._setting

    def __repr__(self):
        return str(self)

    def urlencode(self) -> str:
        """
        Encode setting to match the format in tbs argument of google image search URL.
        Simply returns the setting_str as it was given.
        
        :return: Setting encoded to match the format in tbs argument of google image search URL
        """
        return self._setting

    def __add__(self, other):
        if isinstance(other, QuerySettings):
            return other + self
        if isinstance(other, self.__class__):
            return QuerySettings(self, other)


class QuerySettings:

    """
    General class to represent multiple advanced search options.
    """

    def __init__(self, *settings: str or QuerySetting or "QuerySettings"):
        """
        Class to represent multiple advanced search options.
        
        :param settings: Variable amount of QuerySetting, QuerySettings objects or strings.  
        """
        self._settings = list(*settings)

    def __str__(self):
        return " and ".join(str(setting) for setting in self._settings)

    def __repr__(self):
        return str(self)

    def urlencode(self) -> str:
        """ 
        Encode settings to match the format in **tbs** argument of google image search URL.

        :return: Setting encoded to match the format in tbs argument of google image search URL
        """
        return ",".join(setting.urlencode() for setting in self._settings)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            ret = QuerySettings()
            ret._settings = self._settings + other._settings
            return ret
        if isinstance(other, QuerySetting):
            ret = QuerySettings()
            ret._settings = self._settings[:]
            ret._settings.append(other)
            return ret


class Size:

    """
    Collection of **image size** restrictions that can be used in advanced search options. 
    """

    def __init__(self):
        """This class was not meant to be instanced."""
        raise NotImplementedError("The {} class is not meant to be instanced.".format(self.__class__.__name__))

    ANY = QuerySetting("")
    """Any size, doesn't effect search results."""
    LARGE = QuerySetting("isz:l")
    """Restrict search to large images"""
    MEDIUM = QuerySetting("isz:m")
    """Restrict search to medium images."""
    ICON = QuerySetting("isz:i")
    """Restrict search to icons."""

    @staticmethod
    def exactly(w: int, h: int) -> QuerySetting:
        """
        Restrict search to images of exact size.

        :param w: Required image width
        :param h: Required image height
        :return: QuerySetting representing desired restriction
        """
        return QuerySetting("isz:ex,iszw:{},iszh:{}".format(w, h))

    class LargerThen:

        """
        Collection of **larger-then image size** restrictions.
        """

        def __init__(self):
            """This subclass was not meant to be instanced."""
            raise NotImplementedError("The {} class is not meant to be instanced.".format(self.__class__.__name__))

        S_400x300 = QuerySetting("isz:lt,islt:qsvga")
        """Restrict search to QSVGA (400x300) images."""
        S_640x480 = QuerySetting("isz:lt,islt:vga")
        """Restrict search to VGA (640x480) images."""
        S_800x600 = QuerySetting("isz:lt,islt:svg")
        """Restrict search to SVG (800x600) images."""
        S_1024x768 = QuerySetting("isz:lt,islt:xga")
        """Restrict search to XGA (1024x768) images."""

        QSVGA = S_400x300
        """Restrict search to QSVGA (400x300) images."""
        VGA = S_640x480
        """Restrict search to VGA (640x480) images."""
        SVG = S_800x600
        """Restrict search to SVG (800x600) images."""
        XGA = S_1024x768
        """Restrict search to XGA (1024x768) images."""

        MP_2 = QuerySetting("isz:lt,islt:2mp")
        """Restrict search to 2MP images."""
        MP_4 = QuerySetting("isz:lt,islt:4mp")
        """Restrict search to 4MP images."""
        MP_6 = QuerySetting("isz:lt,islt:6mp")
        """Restrict search to 6MP images."""
        MP_8 = QuerySetting("isz:lt,islt:8mp")
        """Restrict search to 8MP images."""
        MP_10 = QuerySetting("isz:lt,islt:10mp")
        """Restrict search to 10MP images."""
        MP_12 = QuerySetting("isz:lt,islt:12mp")
        """Restrict search to 12MP images."""
        MP_15 = QuerySetting("isz:lt,islt:15mp")
        """Restrict search to 15MP images."""
        MP_20 = QuerySetting("isz:lt,islt:20mp")
        """Restrict search to 20MP images."""
        MP_40 = QuerySetting("isz:lt,islt:40mp")
        """Restrict search to 40MP images."""
        MP_70 = QuerySetting("isz:lt,islt:70mp")
        """Restrict search to 70MP images."""


class Color:

    """
    Collection of **dominant image color** restrictions that can be used in advanced search options. 
    """

    def __init__(self):
        raise NotImplementedError("The {} class is not meant to be instanced.".format(self.__class__.__name__))

    ANY = QuerySetting("")
    """No color restrictions, doesn't effect search results."""
    FULL = QuerySetting("ic:color")
    """Restrict search to full color images."""
    GRAY_SCALE = QuerySetting("ic:gray")
    """Restrict search to black and white images."""
    TRANSPARENT = QuerySetting("ic:trans")
    """Restrict search to partially transparent images."""

    RED = QuerySetting("ic:specific,isc:red")
    """Restrict search to dominantly red images."""
    ORANGE = QuerySetting("ic:specific,isc:orange")
    """Restrict search to dominantly orange images."""
    YELLOW = QuerySetting("ic:specific,isc:yellow")
    """Restrict search to dominantly yellow images."""
    GREEN = QuerySetting("ic:specific,isc:green")
    """Restrict search to dominantly green images."""
    TEAL = QuerySetting("ic:specific,isc:teal")
    """Restrict search to dominantly teal images."""
    BLUE = QuerySetting("ic:specific,isc:blue")
    """Restrict search to dominantly blue images."""
    PURPLE = QuerySetting("ic:specific,isc:purple")
    """Restrict search to dominantly purple images."""
    PINK = QuerySetting("ic:specific,isc:pink")
    """Restrict search to dominantly pink images."""
    WHITE = QuerySetting("ic:specific,isc:white")
    """Restrict search to dominantly white images."""
    GRAY = QuerySetting("ic:specific,isc:gray")
    """Restrict search to dominantly gray images."""
    BLACK = QuerySetting("ic:specific,isc:black")
    """Restrict search to dominantly black images."""
    BROWN = QuerySetting("ic:specific,isc:brown")
    """Restrict search to dominantly brown images."""


class Type:

    """
    Collection of **image type** restrictions that can be used in advanced search options. 
    """

    def __init__(self):
        raise NotImplementedError("The {} class is not meant to be instanced.".format(self.__class__.__name__))

    ANY = QuerySetting("")
    """No type restrictions, doesn't effect search results."""
    FACE = QuerySetting("itp:face")
    """Restrict search to images of faces."""
    PHOTO = QuerySetting("itp:photo")
    """Restrict search to photos."""
    CLIP_ART = QuerySetting("itp:clipart")
    """Restrict search to clipart."""
    LINE_DRAWING = QuerySetting("itp:lineart")
    """Restrict search to lineart."""


class Time:

    """
    Collection of **image upload time** restrictions that can be used in advanced search options. 
    """

    def __init__(self):
        raise NotImplementedError("The {} class is not meant to be instanced.".format(self.__class__.__name__))

    ANY = QuerySetting("")
    """No time restrictions, doesn't effect search results."""
    PAST_SECOND = QuerySetting("qdr:d")
    """Restrict search to images that were uploaded in the past second."""
    PAST_24H = QuerySetting("qdr:d")
    """Restrict search to images that were uploaded in the past 24 hours."""
    PAST_WEEK = QuerySetting("qdr:w")
    """Restrict search to images that were uploaded in the past week."""

    _valid_measures = "nhdwm"

    @staticmethod
    def past(amount: int, unit="h"):
        """
        Restrict search to images that were uploaded in the past <amount> <unit>.
        
        To get results from the past 10 weeks you would add the restriction:
        >>> from gidown.advanced import Time
        >>> Time.past(10, "w")
        tbs=qdr:10w
        
        Allowed units of time:
        
        * n - minute
        * h - hour
        * d - day
        * w - week
        * m - month

        :param amount: Amount of time to look into the past, measured <unit>.
        :param unit: One of the allowed units of time. Defaults to hour (h).
        :return: QuerySetting representing desired restriction.
        """
        if unit not in Time._valid_measures:
            raise ValueError("Unknown measure {}, must be one of: {}".format(unit, Time._valid_measures))
        return QuerySetting("tbs=qdr:{}{}".format(unit, "" if amount <= 1 else amount))

    @staticmethod
    def range(date_from: datetime.date, date_to: datetime.date) ->QuerySetting:
        """
        Generates generic time restrictions. Include images uploaded from <date_from> to <date_to>.

        :param date_from: Starting date, inclusive.
        :param date_to: Ending date, inclusive.
        :return: QuerySetting representing desired restriction.
        """
        return QuerySetting("cdr=1,cd_min={}.{}.{},cd_max={}.{}.{}".format(
            date_from.day, date_from.month, date_from.year, date_to.day, date_to.month, date_to.year))


class FileFormat:

    """
    Collection of **file format** restrictions that can be used in advanced search options.
    """

    def __init__(self):
        raise NotImplementedError("The {} class is not meant to be instanced.".format(self.__class__.__name__))

    ANY = QuerySetting("")
    """No format restrictions, doesn't effect search results."""
    JPG = QuerySetting("ift:jpg")
    """Restrict search to JPG files."""
    GIF = QuerySetting("ift:gif")
    """Restrict search to GIF files."""
    PNG = QuerySetting("ift:png")
    """Restrict search to PNG files."""
    BMP = QuerySetting("ift:mbp")
    """Restrict search to BMP files."""
    SVG = QuerySetting("ift:svg")
    """Restrict search to SVG files."""
    WEBP = QuerySetting("ift:webp")
    """Restrict search to WEBP files."""
    ICO = QuerySetting("ift:ico")
    """Restrict search to ICO files."""


class AspectRatio:

    """
    Collection of **aspect ratio** restrictions that can be used in advanced search options.
    """

    def __init__(self):
        raise NotImplementedError("The {} class is not meant to be instanced.".format(self.__class__.__name__))

    ANY = QuerySetting("")
    """No aspect ratio restrictions, doesn't effect search results."""
    TALL = QuerySetting("iar:t")
    """Restrict search to tall images. (width < height)"""
    SQUARE = QuerySetting("iar:s")
    """Restrict search to square images. (width == height)"""
    WIDE = QuerySetting("iar:w")
    """Restrict search to wide images. (width > height)"""
    PANORAMIC = QuerySetting("iar:xw")
    """Restrict search to panoramic images. (width >> height)"""


class UsageRights:

    """
    Collection of **Usage rights** restrictions that can be used in advanced search options.
    """

    def __init__(self):
        raise NotImplementedError()

    ANY = QuerySetting("")
    """No usage rights restriction, doesn't effect search results."""
    REUSE_WITH_MODIFICATION = QuerySetting("sur:fc")
    """Restrict search to images that can be used commercially with modification"""
    REUSE = QuerySetting("sur:fmc")
    """Restrict search to images that can be used commercially without modification"""
    NONCOMMERCIAL_REUSE_WITH_MODIFICATION = QuerySetting("sur:fm")
    """Restrict search to images that can be used non-commercially with modification"""
    NONCOMMERCIAL_REUSE = QuerySetting("sur:f")
    """Restrict search to images that can be used non-commercially without modification"""


class Sorting:

    """
    Collection of **sorting** options that can be used in advanced search options.
    """

    def __init__(self):
        raise NotImplementedError("The {} class is not meant to be instanced.".format(self.__class__.__name__))

    BY_DATE = QuerySetting("sbd:1")
    """Sort results by date."""
    BY_RELEVANCE = QuerySetting("sbd:0")
    """Sort results by relevance."""
