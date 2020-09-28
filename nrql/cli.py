#!/usr/bin/python3
"""
nrql-cli - An interactive command line interface for querying Insights event data.
"""

from __future__ import unicode_literals

import json
import sys
from argparse import ArgumentParser

from halo import Halo
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments import highlight, lexers, formatters
from pygments.lexers.sql import SqlLexer

from .api import NRQL
from .utils import load_or_generate


def arg_parser():
    """
    Argument parser.
    :return: arr
    """
    parser = ArgumentParser(prog="nrql_cli")
    parser.add_argument(
        "--region",
        "--r",
        default="US",
        choices=["EU", "US"],
        help="Set your region (EU or US) By default the region is set to US.",
    )
    parser.add_argument("--env", "--e", help="Environment handler.")
    parser.add_argument(
        "--verbose",
        "--v",
        dest="verbose",
        action="store_true",
        default=False,
        help="Output the whole response.",
    )
    args = parser.parse_args()
    return args


def main():
    """
    usage: nrql [-h] [--region {EU,US}] [--env ENV] [--verbose]

    optional arguments:
      -h, --help            show this help message and exit
      --region {EU,US}, --r {EU,US}
                            Pass this flag to set your region (EU or US) By
                            default the region is set to US.
      --env ENV, --e ENV    Environment handler.
      --verbose, --v        Pass this flag if you want the whole response.
        :return:
    """
    style = Style.from_dict(
        {
            "completion-menu.completion": "bg:#008888 #ffffff",
            "completion-menu.completion.current": "bg:#00aaaa #000000",
            "scrollbar.background": "bg:#88aaaa",
            "scrollbar.button": "bg:#222222",
        }
    )
    args = arg_parser()
    nrql = NRQL()
    nrql.verbose = args.verbose
    nrql.region = args.region
    wordlist = load_or_generate()
    nrql_completer = WordCompleter(wordlist, ignore_case=True)
    session = PromptSession(
        lexer=PygmentsLexer(SqlLexer), completer=nrql_completer, style=style
    )
    print("Welcome to your data, let's get querying...")
    while True:
        try:
            text = session.prompt("> ")
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            if not (text and text.strip()):
                continue
            if text == "quit()":
                sys.exit(0)
            spinner = Halo(spinner="dots")
            spinner.start()
            req = nrql.query(text)
            spinner.stop()
            formatted_json = json.dumps(req, sort_keys=True, indent=4)
            print(
                highlight(
                    str(formatted_json).encode("utf-8"),
                    lexers.JsonLexer(),
                    formatters.TerminalFormatter(),
                )
            )


if __name__ == "__main__":
    main()
