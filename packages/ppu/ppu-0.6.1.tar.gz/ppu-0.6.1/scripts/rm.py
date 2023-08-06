#! /usr/bin/env python

import argparse
import os
import shutil

try:
    raw_input
except NameError:  # Python 3
    raw_input = input


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remove files/directories')
    parser.add_argument('-f', '--force', action='store_true',
                        help='force (ignore non-existing files and errors)')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='remove directories recursively')
    parser.add_argument('names', nargs='+',
                        help='files/directories names to remove')
    args = parser.parse_args()

    for name in args.names:
        if args.force and not os.path.exists(name):
            continue
        is_dir = os.path.isdir(name)
        if not args.force and not os.access(name, os.W_OK):
            if is_dir:
                ftype = 'directory'
            else:
                ftype = 'file'
            try:
                while True:
                    rmw = raw_input(
                        "rm.py: remove write-protected %s '%s'? [y/n] "
                        % (ftype, name))
                    answer = rmw[:1].lower()
                    if answer == 'y':
                        break
                    elif answer == 'n':
                        raise StopIteration
                    else:
                        continue
            except StopIteration:
                continue
        if is_dir:
            if args.recursive:
                shutil.rmtree(name, args.force)
            else:
                os.rmdir(name)
        else:
            os.unlink(name)
