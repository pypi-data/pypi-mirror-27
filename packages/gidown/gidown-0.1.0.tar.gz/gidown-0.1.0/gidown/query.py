"""
gidown.query
~~~~~~~~~~~~
This module implements advances query options such as site restriction and excluding words.

:license: Apache2, see LICENSE for more details.
"""
from io import StringIO


def all_of(*words: str) -> str:
    """
    Format words to query results containing all the desired words.

    :param words: List of desired words
    :return: String in the format google understands
    """
    return " ".join(*words)


def phrase(term: str) -> str:
    """
    Format words to query results containing the desired phrase.
    
    :param term: A phrase that appears in that exact form. (e.q. phrase "Chicago Bulls" vs. words "Chicago" "Bulls")
    :return: String in the format google understands
    """
    return '"{}"'.format(term)


def any_of(*words: str) -> str:
    """
    Format words to query results containing any the desired words.
    
    :param words: List of desired words
    :return: String in the format google understands
    """
    return " OR ".join(*words)


def none_of(*words: str) -> str:
    """
    Format words to query results containing none of the undesired words.
    This also works with the **on_site** restriction to exclude undesired domains.

    :param words: List of undesired words
    :return: String in the format google understands
    """
    return " ".join("-{}".format(word) for word in words)


def on_site(domain: str) -> str:
    """
    Restrict search to a specific domain.
    Can be repeated to restrict search on multiple sites.

    :param domain: Domain name
    :return: String in the format google understands
    """
    return "site:{}".format(domain)


class QueryBuilder:
    """
    Class for building queries similar to StringBuilder in Java. 
    
    Calling any function defined in :class:`str` on this class returns a string.

    >>> from gidown.query import QueryBuilder
    >>> q = QueryBuilder("text    ")
    >>> q.strip()
    'text'
    
    The query: *dog OR cat eats "ice cream" site:example.com* can be generated with:
    >>> from gidown.query import all_of, any_of, phrase, on_site
    >>> all_of(any_of("dog", "cat"), "eats", phrase("ice cream"), on_site("example.com"))
    
    or with:
    >>> from gidown.query import QueryBuilder
    >>> QueryBuilder().add_choice("dog", "cat").add("eats").add_phrase("ice cream").add_site_restriction("example.com")
       
    """

    def __init__(self, initial_query=""):
        self._query = StringIO()
        print(initial_query.strip(), sep=" ", end=" ", file=self._query)

    def add(self, *words) -> "QueryBuilder":
        """
        Add words to query.
        
        Wrapper around `gis.query.all_of`.

        :param words: Desired words
        :return: self
        """

        print(all_of(*words), sep=" ", end=" ", file=self._query)
        return self

    def add_phrase(self, term) -> "QueryBuilder":
        """
        Add a specific phrase to the query.
        
        Wrapper around `.gis.query.phrase`.

        :param term: Desired phrase
        :return: self
        """
        print(phrase(term), sep=" ", end=" ", file=self._query)
        return self

    def add_choice(self, *words) -> "QueryBuilder":
        """
        Add words to query as *any of*.

        Wrapper around gis.query.any_of.
        
        :param words: Desired words
        :return: self
        """
        print(any_of(*words), sep=" ", end=" ", file=self._query)
        return self

    def exclude(self, *words) -> "QueryBuilder":
        """
        Exclude results with undesired words.

        Wrapper around gis.query.none_of.

        :param words: 
        :return: self
        """
        print(none_of(*words), sep=" ", end=" ", file=self._query)
        return self

    def add_site_restriction(self, domain, exclude=False) -> "QueryBuilder":
        """
        Restrict search to a specific domain.
        Can be repeated to restrict search on multiple sites.

        Wrapper around gis.query.on_site.
        
        :param domain: Domain name that is searched.
        :param exclude: Exclude results from this site.
        :return: self
        """
        print(on_site(domain) if not exclude else none_of(on_site(domain)), sep=" ", end=" ", file=self._query)
        return self

    def __str__(self):
        return self._query.getvalue().strip()

    def __getattr__(self, name):
        if hasattr(str, name):
            func = getattr(str, name)
            return lambda *args, **kwargs: func(str(self), *args, **kwargs)
        raise AttributeError(name)
