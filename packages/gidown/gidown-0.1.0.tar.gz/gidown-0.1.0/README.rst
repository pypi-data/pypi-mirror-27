Google Image Download library
=============================

.. inclusion-marker

Simple library to ease searching for images on Google. The results are
restricted to the first 100 images (depending on the query and advanced
options there might be less results).

Installation
------------

To install all requirements run:

.. code:: bash

    pip install -r requirements.txt 

Usage
-----

To download 5 images of cats and save them, you can run:

.. code:: python

    from gidown import image_query

    images = image_query("cat")
    for i, image in enumerate(images[:5]):
        image.save("img_{}".format(i), auto_ext=True)

File extensions are automatically detected from the image data or, if
that fails, directly from the results of the image search as Google was
kind enough to provide information about the image:

-  image (and thumbnail) URL - ``image.url``, ``image.tb_url``
-  source URL - ``image.src_url``
-  source domain - ``image.src_domain``
-  image type (file extension) - ``image.type``, ``image.tb_type``
-  image (and thumbnail) width - ``image.width``, ``image.tb_width``
-  image (and thumbnail) height - ``image.height``, ``image.tb_height``
-  title (as on the search results page) - ``image.title``
-  description (as on the search results page) - ``image.desc``

All this information can be accesses from the ``GoogleSearchImage``
object, a list of which is returned by ``image_query``. *Image* and
*thumbnail* are not downloaded automatically to save bandwidth. While
saving images with ``image.save``, the image will be automatically
downloaded, if it wasn’t done previously with ``image.download``.

Advanced search options
~~~~~~~~~~~~~~~~~~~~~~~

Google offers a way to filter images by

-  size - ``gidown.advanced.Size``
-  color - ``gidown.advanced.Color``
-  type - ``gidown.advanced.Type``
-  upload time - ``gidown.advanced.Time``
-  usage rights - ``gidown.advanced.UsageRights``
-  format - ``gidown.advanced.FileFormat``

and sort them by relevance or upload time (``gidown.advanced.Sorting``).

To get **large**, **JPG** images that are **mostly red** our previous
search can be modified:

.. code:: python

    from gidown import image_query
    from gidown.advanced import Size, FileFormat, Color

    images = image_query("cat", Size.LARGE, FileFormat.JPG, Color.RED)

Every Google search supports advanced query options, such as:

-  results related to any of query words (e.q. *cat OR dog*) -
   ``gis.query.any_of``
-  exclude results with words (e.q. *cat -dog*) - ``gis.query.none_of``
-  results with exact phrase (e.q. *“small cat on tree”*) -
   ``gis.query.phrase``
-  results only from specific sites (e.q. *cat site:wikipedia.com*)
   ``gis.query.on_site``

   -  can also be used to exclude sites (e.q. *cat -site:wikipedia.com*)

These options are also available via the ``gis.QueryBuilder`` object.

To get large motivational images of cats or dogs:

.. code:: python

    from gidown import image_query
    from gidown.advanced import Size

    # method 1
    from gidown.query import any_of, all_of
    images = image_query(all_of("motivational", any_of("cat", "dog")),
                         Size.LARGE)

    # method 2
    from gidown import QueryBuilder
    q = QueryBuilder().add("motivational").add_choice("cat", "dog")
    images = image_query(q, Size.LARGE)

