"""
Module that implements a simple interface for accessing Google Image Search.

File extensions are automatically determined from the image data or, if that fails,
directly from the results of the image search, as Google wa kind enough to provide a JSON with all information
about the image (image URL, source page URL, Type, Width, Height, Thumbnail URL, ...).

"""

from gidown.search import *
from gidown.query import QueryBuilder
