#!/usr/bin/python
# encoding = utf-8
"""
Generate the HTML for the #ITPE master post.

Usage:
  itpe_generator.py --input <INPUT> [--output <OUTPUT>] [--width=<width>]
  itpe_generator.py (-h | --help)
  itpe_generator.py --version

Options:
  -h --help        Show this screen.
  --input          CSV file containing the ITPE data.
  --output         HTML file for writing the generated HTML.
  --width=<width>  Width of the cover art in px [default: 500px].

"""

import collections
import csv
import os
import re

from jinja2 import Environment, PackageLoader

from .dreamwidth import render_user_links


# Headings for the CSV fields. These don't have to exactly match the spelling/
# spacing of the CSV, but the order should be the same. We define a set of
# heading names here so that we have consistent names to use in the script
HEADINGS = [
    'from_user',
    'for_user',
    'cover_art',
    'cover_artist',
    'editor',
    'title',
    'title_link',
    'authors',
    'fandom',
    'pairing',
    'warnings',
    'length',
    'mp3_link',
    'podbook_link',
    'podbook_compiler',
]

Podfic = collections.namedtuple('Podfic', HEADINGS)


def condense_into_single_line(text):
    """
    Remove all the newlines from a block of text, compressing multiple
    lines of HTML onto a single line.  Used as a Jinja2 filter.
    """
    lines = [line.lstrip() for line in text.split('\n')]
    return ''.join(lines)


def get_jinja2_template():
    """Set up the Jinja2 environment."""
    env = Environment(loader=PackageLoader('itpe', 'templates'),
                      trim_blocks=True)

    env.filters['condense'] = condense_into_single_line
    env.filters['userlinks'] = render_user_links

    template = env.get_template('podfic_template.html')

    return template


def get_podfics(input_file):
    """Read a CSV file and return a list of Podfic instances."""
    podfics = []

    with open(input_file) as csvfile:
        itpereader = csv.reader(csvfile, delimiter=',')

        # Skip the first row, which only contains headings
        next(itpereader)

        for idx, row in enumerate(itpereader):
            print("Reading row %d..." % idx)

            # If we pass the incorrect number of arguments to Podfic,
            # it throws a TypeError.
            try:
                podfic = Podfic(*row)
            except TypeError:
                raise ValueError(
                    "Row %d has the wrong number of entries" % idx)

            podfics.append(podfic)

    return podfics


def main():

    from docopt import docopt
    arguments = docopt(__doc__, version="ITPE 2015.1")

    # Strip everything except the digits from the width option, then append
    # 'px' for the CSS attribute
    arguments['--width'] = re.sub(r'[^0-9]', '', arguments['--width']) + "px"

    # If the caller doesn't give us an output path, guess one based on the
    # input file
    if arguments['<OUTPUT>'] is None:
        basepath, _ = os.path.splitext(arguments['<INPUT>'])
        arguments['<OUTPUT>'] = basepath + '.html'

    template = get_jinja2_template()

    # Get a list of podfics from the input CSV file
    podfics = get_podfics(arguments['<INPUT>'])

    # Turn those podfics into HTML
    podfic_html = (
        template.render(podfic=podfic, width=arguments['--width'])
        for podfic in podfics
    )

    # Write the output HTML, with a <br /> between items to add space
    # in the rendered page.
    with open(arguments['<OUTPUT>'], 'w') as outfile:
        outfile.write('\n<br />\n'.join(podfic_html))

    print("HTML has been written to %s." % arguments['<OUTPUT>'])


if __name__ == '__main__':
    main()
