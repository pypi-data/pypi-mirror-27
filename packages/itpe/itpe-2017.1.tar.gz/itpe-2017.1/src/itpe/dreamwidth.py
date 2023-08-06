#!/usr/bin/env python
"""
If you want to link to another user on Dreamwidth, you can use a
<user> tag, which gets annotated with a small icon to show that
it's another Dreamwidth account:

    <user name=amplificathon>

You can also specify a site attribute with a variety of services, which
add service-appropriate icons:

    <user name=itpe_mod site=twitter.com>

See the Dreamwidth FAQs: http://www.dreamwidth.org/support/faqbrowse?faqid=87

The ITPE template uses a compact syntax, prefixing a username with an
abbreviation and a slash, e.g. "tum/staff" or "tw/support".

This file contains a function for turning these templae strings into
the full <user> tags.
"""

import unittest
from unittest.mock import patch, MagicMock

from jinja2 import Template
import termcolor


SITE_PREFIXES = {
    'ao3':  'archiveofourown.org',
    'blog': 'blogspot.com',
    'dj':   'deadjournal.com',
    'del':  'delicious.com',
    'dev':  'deviantart.com',
    'dw':   'dreamwidth.org',
    'da':   'da',
    'etsy': 'etsy.com',
    'ff':   'fanfiction.net',
    'ink':  'inksome.com',
    'ij':   'insanejournal.com',
    'jf':   'journalfen.com',
    'last': 'last.fm',
    'lj':   'livejournal.com',
    'pin':  'pinboard.in',
    'pk':   'plurk.com',
    'rvl':  'ravelry.com',
    'tw':   'twitter.com',
    'tum':  'tumblr.com',
    'wp':   'wordpress.com'
}

USERLINK = Template("<user name={{ name }}{% if site and "
                    "site != 'dreamwidth.org' %} site={{ site }}{% endif %}>")

SPECIAL_CASE_NAMES = [
    '(various)',
    'anonymous'
]


def warn(message):
    termcolor.cprint(message, color='yellow')


def _single_user_link(user_str):
    """Renders a short username string into an HTML <user> link."""

    if not user_str.strip():
        warn("Skipping empty user string.")
        return ''

    # If there's a space in the user string, then we drop through a raw
    # string (e.g. "the podfic community")
    if (' ' in user_str) or (user_str.lower() in SPECIAL_CASE_NAMES):
        warn("Skipping user string '%s'" % user_str)
        return user_str

    # If there aren't any slashes, then treat it as a Dreamwidth user
    if '/' not in user_str:
        warn("No site specified for '%s'; assuming Dreamwidth" % user_str)
        return USERLINK.render(name=user_str)

    # If there's one slash, split the string and work out the site name.
    # Throws a ValueError if there's more than one slash.
    try:
        short_site, name = user_str.split('/')
    except ValueError:
        raise ValueError("Invalid user string '%s'" % user_str)

    try:
        site = SITE_PREFIXES[short_site]
    except KeyError:
        raise ValueError("Invalid site prefix in string '%s'" % user_str)

    # If it's a Dreamwidth user, we don't need to specify the site attribute
    return USERLINK.render(name=name, site=site)


def render_user_links(name_str):
    """
    Takes a string of names, possibly separated with commas or ampersands,
    and returns an appropriate string of <user> tags.
    """
    if '&' in name_str:
        components = (render_user_links(part.strip())
                      for part in name_str.split('&'))
        return ' & '.join(c for c in components if c)
    else:
        components = (_single_user_link(name.strip())
                      for name in name_str.split(','))
        return ', '.join(c for c in components if c)


class UserLinkTests(unittest.TestCase):

    def setUp(self):
        self.cprint = patch('termcolor.cprint', new=MagicMock())
        self.cprint.start()

    def tearDown(self):
        self.cprint.stop()

    def assert_correct_expansion(self, short_string, expected):
        self.assertEqual(render_user_links(short_string), expected)

    def assert_correct_expansions(self, test_cases):
        for user_str, expected in test_cases:
            self.assertEqual(render_user_links(user_str), expected)

    def test_skipped_strings(self):
        """Strings with spaces or special phrases are skipped."""
        test_cases = [
            (' ', ''),
            ('fish cakes', 'fish cakes'),
            ('anonymous', 'anonymous'),
            ('anonymous cat', 'anonymous cat'),
        ]
        self.assert_correct_expansions(test_cases)

    def test_defaulted_strings(self):
        """Strings without a site prefix default to Dreamwidth."""
        test_cases = [
            ('dog', '<user name=dog>'),
            ('fish', '<user name=fish>'),
            ('horse', '<user name=horse>'),
            ('gerbil', '<user name=gerbil>'),
        ]
        self.assert_correct_expansions(test_cases)

    def test_invalid_strings(self):
        """Strings with >1 slash raise a ValueError."""
        for bad_string in ['parrot/budgie/parakeet', 'cat///mouse']:
            with self.assertRaises(ValueError):
                render_user_links(bad_string)

    def test_invalid_prefixes(self):
        """Strings with an unknown site prefix raise a ValueError."""
        for bad_string in ['nope/turtle', 'bad/tortoise', '/reptile']:
            with self.assertRaises(ValueError):
                render_user_links(bad_string)

    def test_dreamwidth_strings(self):
        """Strings with the dw/ prefix don't include a site= attribute."""
        test_cases = [
            ('dw/ferret', '<user name=ferret>'),
            ('dw/rabbit', '<user name=rabbit>'),
            ('dw/bunny', '<user name=bunny>'),
        ]
        self.assert_correct_expansions(test_cases)

    def test_other_strings(self):
        """Strings with non-dw/ prefixes include a site= attribute."""
        test_cases = [
            ('tw/snake', '<user name=snake site=twitter.com>'),
            ('ao3/newt', '<user name=newt site=archiveofourown.org>'),
            ('tum/iguana', '<user name=iguana site=tumblr.com>'),
        ]
        self.assert_correct_expansions(test_cases)

    def test_commas_strings(self):
        """Comma-separated strings render correctly."""
        test_cases = [
            (
                'lion, ff/tiger',
                '<user name=lion>, <user name=tiger site=fanfiction.net>'
            ),
            (
                'panther, cheetah, puma',
                '<user name=panther>, <user name=cheetah>, <user name=puma>'
            ),
            (
                'lj/lynx,',
                '<user name=lynx site=livejournal.com>'
            ),
        ]
        self.assert_correct_expansions(test_cases)

    def test_amp_strings(self):
        """Ampersand-separated strings render correctly."""
        test_cases = [
            (
                'rhino &',
                '<user name=rhino>'
            ),
            (
                'pin/hippo & elephant',
                '<user name=hippo site=pinboard.in> & <user name=elephant>'
            ),
        ]
        self.assert_correct_expansions(test_cases)

    def test_mixed_strings(self):
        """Strings with commas and ampersands render correctly."""
        test_cases = [
            (
                'fish, squid & clam',
                '<user name=fish>, <user name=squid> & <user name=clam>'
            ),
        ]
        self.assert_correct_expansions(test_cases)


if __name__ == '__main__':
    unittest.main()
