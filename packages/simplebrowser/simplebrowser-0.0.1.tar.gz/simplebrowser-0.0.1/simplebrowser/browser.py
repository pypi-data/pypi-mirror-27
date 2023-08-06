import requests
from bs4 import BeautifulSoup, SoupStrainer


class BrowserError(Exception):
    pass


class ParsingError(BrowserError):
    pass


class NoWebsiteLoadedError(BrowserError):
    pass


class SimpleBrowser:
    """Low-level HTTP browser to simplify interacting with websites.

    Attributes:
        parser: Used in website parsing, defaults to `lxml`.
        session: A reusable TCP connection, useful for making requests to the
            same website and managing cookies.
            <http://docs.python-requests.org/en/master/user/advanced/#session-objects>
        url: Full URL of currently loaded website.
        response: Response of currently loaded website.
    """
    def __init__(self, parser='lxml'):
        self.parser = parser
        self.session = requests.Session()
        self._url = None
        self._response = None

    @property
    def url(self):
        """Return the URL of currently loaded website."""
        return self._url

    @property
    def response(self):
        """Return the `Response` object of currently loaded website."""
        return self._response

    @property
    def cookies(self):
        """Return the CookieJar instance of the current `Session`."""
        return self.session.cookies

    def soup(self, *args, **kwargs):
        """Parse the currently loaded website.

        Optionally, SoupStrainer can be used to only parse relevant
        parts of the page. This can be particularly useful if the website is
        complex or perfomance is a factor.
        <https://www.crummy.com/software/BeautifulSoup/bs4/doc/#soupstrainer>

        Args:
            *args: Optional positional arguments that `SoupStrainer` takes.
            **kwargs: Optional keyword argument that `SoupStrainer` takes.

        Returns:
            A `BeautifulSoup` object.

        Raises:
            NoWebsiteLoadedError: If no website is currently loaded.
            ParsingError: If the current response isn't supported by `bs4`
        """
        if self._url is None:
            raise NoWebsiteLoadedError('website parsing requires a loaded website')

        content_type = self._response.headers.get('Content-Type', '')
        if not any(markup in content_type for markup in ('html', 'xml')):
            raise ParsingError('unsupported content type \'{}\''.format(content_type))

        strainer = SoupStrainer(*args, **kwargs)
        return BeautifulSoup(self._response.content, self.parser, parse_only=strainer)

    def get(self, url, **kwargs):
        """Send a GET request to the specified URL.

        Method directly wraps around `Session.get` and updates browser
        attributes.
        <http://docs.python-requests.org/en/master/api/#requests.get>

        Args:
            url: URL for the new `Request` object.
            **kwargs: Optional arguments that `Request` takes.

        Returns:
            `Response` object of a successful request.
        """
        response = self.session.get(url, **kwargs)
        self._url = response.url
        self._response = response
        return response

    def post(self, **kwargs):
        """Send a POST request to the currently loaded website's URL.

        The browser will automatically fill out the form. If `data` dict has
        been passed into ``kwargs``, the contained input values will override
        the automatically filled out values.

        Returns:
            `Response` object of a successful request.

        Raises:
            NoWebsiteLoadedError: If no website is currently loaded.
        """
        if self._url is None:
            raise NoWebsiteLoadedError('request submission requires a loaded website')

        data = kwargs.get('data', {})
        for i in self.soup('form').select('input[name]'):
            if i.get('name') not in data:
                data[i.get('name')] = i.get('value', '')
        kwargs['data'] = data

        response = self.session.post(self._url, **kwargs)
        self._url = response.url
        self._response = response
        return response
