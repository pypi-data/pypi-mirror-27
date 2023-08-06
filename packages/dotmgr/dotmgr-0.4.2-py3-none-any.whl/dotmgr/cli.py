#!/usr/bin/env python3
#
# This file is part of dotmgr.
#
# dotmgr is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# dotmgr is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with dotmgr.  If not, see <http://www.gnu.org/licenses/>.
"""Dotfile manager CLI

A small script that can help you maintain your dotfiles across several devices.
"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter, REMAINDER
from sys import argv
from textwrap import dedent, indent

from dotmgr.manager import Manager
from dotmgr.paths import DEFAULT_DOTFILE_REPOSITORY_PATH, DEFAULT_DOTFILE_TAG_CONFIG_PATH, \
                         prepare_dotfile_repository_path, prepare_tag_config_path
from dotmgr.repository import Repository
from pkg_resources import require

def get_version():
    """Returns the program version."""
    return require('dotmgr')[0].version

def prepare_argument_parser():
    """Creates and configures the argument parser for the CLI.
    """
    parser = ArgumentParser(usage=indent(dedent("""
                    dotmgr [-h]
                    dotmgr [-v] -I           [path]
                    dotmgr [-v] -A [-c | -s] <path>
                    dotmgr [-v] -D [-c | -s] <path>
                    dotmgr [-v] -G [-c | -s] [path] [message]
                    dotmgr [-v] -S      [-s] [path]
                    dotmgr [-v] -Q <-r | -t>
                    dotmgr [-v] -V <command...>
                            """), '  '),
                            description='Generalize / specialize dotfiles',
                            epilog=dedent("""\
                    default paths and environment variables:
                      General dotfiles are read from / written to {}.
                      You can set the environment variable $DOTMGR_REPO to change this.

                      Tags are read from ~/{}, which can be changed
                      by setting $DOTMGR_TAG_CONF.

                    version:
                      This is version {} of dotmgr.
                            """).format(DEFAULT_DOTFILE_REPOSITORY_PATH,
                                        DEFAULT_DOTFILE_TAG_CONFIG_PATH,
                                        get_version()),
                            formatter_class=RawDescriptionHelpFormatter,
                            add_help=True)
    parser.add_argument('-v', dest='verbose', action='store_true',
                        help='enable verbose output (useful for debugging)')

    acts = parser.add_argument_group('actions').add_mutually_exclusive_group(required=True)
    acts.add_argument('-A', dest='add', action='store_true',
                      help='create a generalized version of a dotfile from your home directory in'
                           'the repository')
    acts.add_argument('-D', dest='delete', action='store_true',
                      help='remove a dotfile from the repository')
    acts.add_argument('-G', dest='generalize', action='store_true',
                      help='generalize a tracked dotfile in your home directory')
    acts.add_argument('-I', dest='init', action='store_true',
                      help='clone a dotfile repository from the given <path> or initialize an '
                           'empty one if <path> is omitted')
    acts.add_argument('-Q', dest='query', action='store_true',
                      help='query certain settings and parameters of dotmgr')
    acts.add_argument('-S', dest='specialize', action='store_true',
                      help='specialize a dotfile from the repository')
    acts.add_argument('-V', dest='command', nargs=REMAINDER, metavar='arg',
                      help='run a git command in the dotfile repository')

    parser.add_argument('path', nargs='?', default=None,
                        help='a relative path to a dotfile - if omitted, the requested action is '
                             'performed for all dotfiles')
    parser.add_argument('message', nargs='?', default=None,
                        help='a commit message for git')

    vcs_opts = parser.add_argument_group('VCS options').add_mutually_exclusive_group()
    vcs_opts.add_argument('-c', dest='commit', action='store_true',
                          help='commit changes to the dotfile repository')
    vcs_opts.add_argument('-s', dest='sync', action='store_true',
                          help='synchronize repository before / after operation (implies -c)')

    query_opts = parser.add_argument_group('query options').add_mutually_exclusive_group()
    query_opts.add_argument('-r', dest='repo', action='store_true',
                            help='the (absolute) path to the dotfile repository')
    query_opts.add_argument('-t', dest='tag_conf', action='store_true',
                            help='the (absolute) path to dotmgr\'s tag configuration file')

    return parser

def dotmgr(args):
    """dotmgr CLI

    Args:
        args ([string]):    command-line arguments
    """
    def add():
        """Helper function for the -A action.
        """
        if not args.path:
            parser.print_usage()
            exit()
        manager.add(args.path, args.commit or args.sync)
        if args.sync:
            repository.push()

    def delete():
        """Helper function for the -D action.
        """
        if not args.path:
            parser.print_usage()
            exit()
        manager.delete(args.path, args.commit or args.sync)
        if args.sync:
            repository.push()

    def generalize():
        """Helper function for the -G action.
        """
        try:
            if args.path:
                manager.generalize(args.path, args.commit or args.sync, args.message)
            else:
                manager.generalize_all(args.commit or args.sync)
        except FileNotFoundError:
            return
        if args.sync:
            repository.push()

    def query():
        """Helper function for the -Q action.
        """
        if args.repo:
            print(dotfile_repository_path)
        elif args.tag_conf:
            print(dotfile_tag_config_path)
        exit()

    def specialize():
        """Helper function for the -S action.
        """
        if args.sync:
            repository.pull()
        if args.path:
            manager.specialize(args.path)
        else:
            manager.specialize_all()

    # Check and parse arguments
    parser = prepare_argument_parser()
    args = parser.parse_args(args)

    # Enable verbose mode if requested
    verbose = False
    if args.verbose:
        verbose = True

    # Prepare paths
    dotfile_repository_path = prepare_dotfile_repository_path(args.init, verbose)
    dotfile_tag_config_path = prepare_tag_config_path(args.init, verbose, dotfile_repository_path)

    # If desired, initialize or clone the dotfile repository and exit
    repository = Repository(dotfile_repository_path, verbose)
    if args.init:
        if args.path:
            repository.clone(args.path)
        else:
            repository.initialize(dotfile_tag_config_path)
        exit()

    # Fire up dotfile manager instance
    manager = Manager(repository, dotfile_tag_config_path, verbose)

    # Execute selected action
    if args.add:
        add()
    elif args.delete:
        delete()
    elif args.generalize:
        generalize()
    elif args.specialize:
        specialize()
    elif args.query:
        query()
    elif args.command:
        repository.execute(args.command)

def main():
    """Program entry point.

    Where things start to happen...
    """
    dotmgr(argv[1:])
