#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import __future__
import argcomplete
import argparse
import os
import sys
import logging
import hashlib
import glob
import tempfile
import zipfile
import shutil
import platform

import appdirs
try:
    from .github_repos import Github_Repos
    from . import flash_dfu
    from . import flash_serial
except Exception:
    from github_repos import Github_Repos
    import flash_dfu
    import flash_serial

try:
    from urllib import urlretrieve
except ImportError:  # Python 3
    from urllib.request import urlretrieve

__version__ = '0.7.0'
SKELETON_URL_ZIP = 'https://github.com/bigclownlabs/bcf-skeleton/archive/master.zip'
SDK_URL_ZIP = 'https://github.com/bigclownlabs/bcf-sdk/archive/master.zip'
SDK_GIT = 'https://github.com/bigclownlabs/bcf-sdk.git'


def print_table(labels, rows):
    if not labels and not rows:
        return

    max_lengths = [0] * (len(rows[0]) if rows else len(labels))
    for i, label in enumerate(labels):
        max_lengths[i] = len(label)

    for row in rows:
        for i, v in enumerate(row):
            if len(v) > max_lengths[i]:
                max_lengths[i] = len(v)

    row_format = "{:<" + "}  {:<".join(map(str, max_lengths)) + "}"

    if labels:
        print(row_format.format(*labels))
        print("=" * (sum(max_lengths) + len(labels) * 2))

    for row in rows:
        print(row_format.format(*row))


def print_progress_bar(title, progress, total, length=20):
    filled_length = int(length * progress // total)
    if filled_length < 0:
        filled_length = 0
    bar = '#' * filled_length
    bar += '-' * (length - filled_length)
    percent = 100 * (progress / float(total))
    if percent > 100:
        percent = 100
    elif percent < 0:
        percent = 0
    sys.stdout.write('\r\r')
    sys.stdout.write(title + ' [' + bar + '] ' + "{:5.1f}%".format(percent))
    sys.stdout.flush()
    if percent == 100:
        sys.stdout.write('\n')
        sys.stdout.flush()


def download_url_reporthook(count, blockSize, totalSize):
    print_progress_bar('Download', count * blockSize, totalSize)


def download_url(url, user_cache_dir, use_cache=True):
    filename = hashlib.sha256(url.encode()).hexdigest()
    filename_bin = os.path.join(user_cache_dir, filename)

    if use_cache and os.path.exists(filename_bin):
        return filename_bin

    print('download firmware from', url)
    print('save as', filename_bin)

    urlretrieve(url, filename_bin, reporthook=download_url_reporthook)

    return filename_bin


class FlashChoicesCompleter(object):
    def __init__(self, find_bin):
        self._find_bin = find_bin

    def __call__(self, **kwargs):
        user_cache_dir = appdirs.user_cache_dir('bcf')
        repos = Github_Repos(user_cache_dir)
        # search = kwargs.get('prefix', None)
        firmwares = repos.get_firmware_list()
        if self._find_bin:
            firmwares += glob.glob('*.bin')
        return firmwares


def command_devices(verbose=False, include_links=False):
    if os.name == 'nt' or sys.platform == 'win32':
        from serial.tools.list_ports_windows import comports
    elif os.name == 'posix':
        from serial.tools.list_ports_posix import comports

    for port, desc, hwid in sorted(comports(include_links=include_links)):
        sys.stdout.write("{:20}\n".format(port))
        if verbose:
            sys.stdout.write("    desc: {}\n".format(desc))
            sys.stdout.write("    hwid: {}\n".format(hwid))


def main():
    parser = argparse.ArgumentParser(description='BigClown Firmware Tool')

    subparsers = {}
    subparser = parser.add_subparsers(dest='command', metavar='COMMAND')

    subparsers['update'] = subparser.add_parser('update', help="update list of available firmware")

    subparsers['list'] = subparser.add_parser('list', help="list firmware")
    subparsers['list'].add_argument('--all', help='show all releases', action='store_true')
    subparsers['list'].add_argument('--description', help='show description', action='store_true')
    subparsers['list'].add_argument('--show-pre-release', help='show pre-release version', action='store_true')

    subparsers['flash'] = subparser.add_parser('flash', help="flash firmware",
                                               usage='%(prog)s\n       %(prog)s <firmware>\n       %(prog)s <file>\n       %(prog)s <url>')
    subparsers['flash'].add_argument('what', help=argparse.SUPPRESS, nargs='?',
                                     default="firmware.bin").completer = FlashChoicesCompleter(True)
    subparsers['flash'].add_argument('--device', help='device', required='--dfu' not in sys.argv)
    subparsers['flash'].add_argument('--dfu', help='use dfu mode', action='store_true')

    subparsers['devices'] = subparser.add_parser('devices', help="show devices")
    subparsers['devices'].add_argument('-v', '--verbose', action='store_true', help='show more messages')
    subparsers['devices'].add_argument('-s', '--include-links', action='store_true', help='include entries that are symlinks to real devices')

    subparsers['search'] = subparser.add_parser('search', help="search in firmware names and descriptions")
    subparsers['search'].add_argument('pattern', help='search pattern')
    subparsers['search'].add_argument('--all', help='show all releases', action='store_true')
    subparsers['search'].add_argument('--description', help='show description', action='store_true')
    subparsers['search'].add_argument('--show-pre-release', help='show pre-release version', action='store_true')

    subparsers['pull'] = subparser.add_parser('pull', help="pull firmware to cache",
                                              usage='%(prog)s <firmware>\n       %(prog)s <url>')
    subparsers['pull'].add_argument('what', help=argparse.SUPPRESS).completer = FlashChoicesCompleter(False)

    subparsers['clean'] = subparser.add_parser('clean', help="clean cache")

    subparsers['create'] = subparser.add_parser('create', help="create new firmware")
    subparsers['create'].add_argument('name', help=argparse.SUPPRESS)
    subparsers['create'].add_argument('--no-git', help='disable git', action='store_true')

    subparsers['read'] = subparser.add_parser('read', help="download firmware to file")
    subparsers['read'].add_argument('filename', help=argparse.SUPPRESS)
    subparsers['read'].add_argument('--device', help='device', required=True)
    subparsers['read'].add_argument('--length', help='length', default=196608, type=int)

    subparser_help = subparser.add_parser('help', help="show help")
    subparser_help.add_argument('what', help=argparse.SUPPRESS, nargs='?', choices=subparsers.keys())

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit()

    if args.command == 'help':
        if args.what:
            subparsers[args.what].print_help()
        else:
            parser.print_help()
        sys.exit()

    user_cache_dir = appdirs.user_cache_dir('bcf')
    repos = Github_Repos(user_cache_dir)

    if args.command == 'list' or args.command == 'search':
        # labels = ['Name:Bin:Version']
        # if args.description:
        #     labels.append('description')

        rows = repos.get_firmware_table(search=args.pattern if args.command == 'search' else None,
                                        all=args.all,
                                        description=args.description,
                                        show_pre_release=args.show_pre_release)

        if rows:
            print_table([], rows)
        else:
            print('Nothing found, try updating first')

    elif args.command == 'flash':
        if args.what.startswith('http'):
            filename_bin = download_url(args.what, user_cache_dir)

        elif os.path.exists(args.what) and os.path.isfile(args.what):
            filename_bin = args.what

        else:
            firmware = repos.get_firmware(args.what)
            if not firmware:
                print('Firmware not found, try updating first')
                sys.exit(1)
            filename_bin = download_url(firmware['download_url'], user_cache_dir)

        if args.dfu:
            flash_dfu.run(filename_bin)
        else:
            try:
                flash_serial.run(args.device, filename_bin, reporthook=print_progress_bar)
            except Exception as e:
                print(e)
                if os.getenv('DEBUG', False):
                    raise e
                sys.exit(1)

    elif args.command == 'update':
        repos.update()

    elif args.command == 'devices':
        command_devices(verbose=args.verbose, include_links=args.include_links)

    elif args.command == 'pull':
        if args.what == 'last':
            for name in repos.get_firmware_list():
                firmware = repos.get_firmware(name)
                print('pull', name)
                download_url(firmware['download_url'], user_cache_dir, True)
                print()

        elif args.what.startswith('http'):
            download_url(args.what, user_cache_dir, True)
        else:
            firmware = repos.get_firmware(args.what)
            if not firmware:
                print('Firmware not found, try updating first, command: bcf update')
                sys.exit(1)
            download_url(firmware['download_url'], user_cache_dir, True)

    elif args.command == 'clean':
        repos.clear()
        for filename in os.listdir(user_cache_dir):
            os.unlink(os.path.join(user_cache_dir, filename))

    elif args.command == 'create':
        name = args.name

        if os.path.exists(name):
            print('Directory already exists')
            sys.exit(1)

        skeleton_zip_filename = download_url(SKELETON_URL_ZIP, user_cache_dir)
        print()

        tmp_dir = tempfile.mkdtemp()

        zip_ref = zipfile.ZipFile(skeleton_zip_filename, 'r')
        zip_ref.extractall(tmp_dir)
        zip_ref.close()

        skeleton_path = os.path.join(tmp_dir, os.listdir(tmp_dir)[0])
        shutil.move(skeleton_path, name)

        os.rmdir(os.path.join(name, 'sdk'))
        os.chdir(name)

        if args.no_git:
            sdk_zip_filename = download_url(SDK_URL_ZIP, user_cache_dir)
            zip_ref = zipfile.ZipFile(sdk_zip_filename, 'r')
            zip_ref.extractall(tmp_dir)
            zip_ref.close()

            sdk_path = os.path.join(tmp_dir, os.listdir(tmp_dir)[0])
            shutil.move(sdk_path, 'sdk')

        else:

            os.system('git init')
            os.system('git submodule add --depth 1 "' + SDK_GIT + '" sdk')

        os.rmdir(tmp_dir)

    elif args.command == 'read':
        flash_serial.clone(args.device, args.filename, args.length, reporthook=print_progress_bar)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
