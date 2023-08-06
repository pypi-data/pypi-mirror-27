#! /usr/bin/env python3

'''
Convert any json input to any output format defined by mako template
'''

from argparse import ArgumentParser
from json import loads
from mako.template import Template
import os
import sys

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "__version__.py")).read())


def json_to_mako_wrapper(args):
    '''
    Main entry for json_to_mako
    '''
    PARSER = ArgumentParser(description='Convert any JSON data base to a mako-templated output.')
    PARSER.add_argument("-v", "--version", action="version", version="%(prog)s " + __version__)
    PARSER.add_argument('-i', '--input', action='append',
                        required=True,
                        help='Input file(s): JSON file(s).')
    PARSER.add_argument('-o', '--output', action='store',
                        required=True,
                        help='Output file.')
    GROUP = PARSER.add_mutually_exclusive_group(required=True)
    GROUP.add_argument('-t', '--template', action='store',
                       help='Custom MAKO template file for which to render the given JSON input.')
    ARGS = PARSER.parse_args(args)

    if ARGS.template:
        TEMPLATE = ARGS.template
    else:
        raise ValueError('No template specified')

    database = []
    for inputfile in ARGS.input:
        with open(inputfile, 'r') as finput:
            database.append(loads(finput.read()))
    tmpl = Template(filename=TEMPLATE)
    rendered = tmpl.render(db=database)
    with open(ARGS.output, 'w') as out:
        out.write(rendered)


def main():
    sys.exit(json_to_mako_wrapper(sys.argv[1:]))


if __name__ == '__main__':
    main()
