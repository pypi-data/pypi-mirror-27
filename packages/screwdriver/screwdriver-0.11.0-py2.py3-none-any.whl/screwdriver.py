__version__ = '0.11.0'

import sys, json
from collections import namedtuple

from six.moves import html_parser 

# =============================================================================
# Utility Methods
# =============================================================================

def dynamic_load(name):
    """Equivalent of "from X import Y" statement using dot notation to specify
    what to import and return.  For example, foo.bar.thing returns the item
    "thing" in the module "foo.bar" """
    pieces = name.split('.')
    item = pieces[-1]
    mod_name = '.'.join(pieces[:-1])

    mod = __import__(mod_name, globals(), locals(), [item])
    return getattr(mod, item)


def camelcase_to_underscore(text):
    prev_cap = text[0].isupper()
    result = [text[0].lower(), ]
    for letter in text[1:]:
        if letter.isupper():
            if not prev_cap:
                result.append('_')

            result.append(letter.lower())
            prev_cap = True
        else:
            result.append(letter)
            prev_cap = False

    return ''.join(result)


def rows_to_columns(matrix):
    """Takes a two dimensional array and returns an new one where rows in the
    first become columns in the second."""
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    data = []
    for i in range(0, num_cols):
        data.append([matrix[j][i] for j in range(0, num_rows)])

    return data


class AnchorParser(html_parser.HTMLParser):
    ParsedLink = namedtuple('ParsedLink', ['url', 'text'])

    def __init__(self, *args, **kwargs):
        if sys.version_info > (3,):
            super(AnchorParser, self).__init__(*args, **kwargs)
        else:   # pragma: no cover
            # html_parser is still an old style object and so super doesn't
            # work
            html_parser.HTMLParser.__init__(self, *args, **kwargs)

        self.capture = 0
        self.url = ''
        self.text = ''

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            self.capture += 1

            if self.capture == 1:
                for attr in attrs:
                    if attr[0] == 'href':
                        self.url = attr[1]
                        break

    def handle_endtag(self, tag):
        if tag.lower() == 'a':
            self.capture += 1

    def handle_data(self, data):
        if self.capture == 1:
            self.text = data


def parse_link(html):
    """Parses an HTML anchor tag, returning the href and content text.  Any
    content before or after the anchor tag pair is ignored.

    :param html:
        Snippet of html to parse
    :returns:
        namedtuple('ParsedLink', ['url', 'text'])

    Example:

    .. code-block:: python

        >>> parse_link('things <a href="/foo/bar.html">Foo</a> stuff')
        ParsedLink('/foo/bar.html', 'Foo')
    """
    parser = AnchorParser()
    parser.feed(html)
    return parser.ParsedLink(parser.url, parser.text)


def pprint(data):
    """Alternative to `pprint.PrettyPrinter()` that uses `json.dumps()` for
    sorting and displaying data.  

    :param data: item to print to STDOUT.  The item must be json serializable!
    """
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
