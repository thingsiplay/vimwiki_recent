#!/bin/env python3

import sys
import os
import pathlib
import argparse


def parse_arguments():

    parser = argparse.ArgumentParser(
        description=('Read your vimwiki files sorted by last used and create '
                     'a list'),
        epilog=('Copyright © 2022 Tuncay D. '
                '<https://github.com/thingsiplay/vimwiki_recent>')
    )

    example = '~/vimwiki'
    parser.add_argument(
        '-d', '--dir',
        metavar='DIR',
        type=pathlib.Path,
        required=True,
        help=('root directory of your vimwiki, '
              f'example: "{example}"'),
    )

    default = 'wiki'
    parser.add_argument(
        '-e', '--ext',
        metavar='EXT',
        default=default,
        help=('file extension without dot of your vimwiki files, '
              f'defaults to "{default}"'),
    )

    default = 'recent'
    parser.add_argument(
        '-r', '--recent',
        metavar='NAME',
        default=default,
        help=('name of recent file to create, basename without extension, '
              f'defaults to "{default}"'),
    )

    default = 'index,diary'
    parser.add_argument(
        '-i', '--ignore',
        metavar='NAMES',
        default=default,
        help=('comma separated list of files and folders to ignore, only '
              f'basename without extension, defaults to "{default}"'),
    )

    parser.add_argument(
        '-X', '--dry-run',
        default=False,
        action='store_true',
        help=('do not write recent file to filesystem')
    )

    parser.add_argument(
        '-o', '--stdout',
        default=False,
        action='store_true',
        help=('print recent content to stdout stream')
    )

    return parser.parse_args()


def read_dir(directory, ext):
    ext = "." + ext
    list_of_files = []
    for path, dirs, files in os.walk(directory):
        for name in files:
            file = pathlib.PurePath(path, name)
            if file.suffix == ext:
                list_of_files.append(file)
    return list_of_files


def sort_files(files):
    files.sort(key=lambda f: os.path.getmtime(f))
    files.reverse()
    return files


def remove_ignored_names(files, ignore_names):
    return [file for file in files if file.stem not in ignore_names]


def files_to_relative_dir(files, relative_dir):
    return [file.relative_to(relative_dir) for file in files]


def file_to_wiki(file):
    link = "[[" + file.as_posix() + "|" + file.stem + "]]"
    if file.parent.stem:
        return link + " (" + file.parent.stem + ")"
    else:
        return link


def convert_to_links(files):
    return [file_to_wiki(file) for file in files]


def write_recent_file(file, content):
    file.write_text("\n".join(content) + "\n")


def write_stdout(content):
    print("\n".join(content))


def path_not_exist(path):
    try:
        if not path.exists():
            raise FileNotFoundError(f'Path does not exist: "{path}"')
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 1
    return 0


def main():

    args = parse_arguments()

    wiki_dir = pathlib.Path(args.dir).expanduser().resolve()
    if path_not_exist(wiki_dir):
        return 1

    recent_file = f"{wiki_dir}/{args.recent}.{args.ext}"
    recent_file = pathlib.Path(recent_file).resolve()
    ignore = args.ignore.split(',') + [args.recent]

    files = read_dir(wiki_dir, args.ext)
    files = sort_files(files)
    files = remove_ignored_names(files, ignore)

    relative_files = files_to_relative_dir(files, wiki_dir)
    wiki_links = convert_to_links(relative_files)

    if not args.dry_run:
        write_recent_file(recent_file, wiki_links)

    if args.stdout:
        write_stdout(wiki_links)

    return 0


if __name__ == '__main__':
    sys.exit(main())
