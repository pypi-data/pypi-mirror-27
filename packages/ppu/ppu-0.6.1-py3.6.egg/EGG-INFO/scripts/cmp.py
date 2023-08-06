#!/usr/bin/env python
"""cmp.py: compare two files. Portable replacement for cmp."""

import argparse
import os
import sys


def report(silent):
    if show_pbar:
        global pbar
        del pbar
    if not silent:
        sys.stderr.write("Files differ at %d megabayte block\n" % count)
    global diff
    diff = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remove old files')
    parser.add_argument('-i', '--inhibit-progress-bar', action='store_true',
                        help='inhibit progress bar')
    parser.add_argument('-s', '--silent', '--quiet', action='store_true',
                        help='be silent (implied -i)')
    parser.add_argument('fname1', help='the first file name')
    parser.add_argument('fname2', help='the second file name')
    args = parser.parse_args()

    show_pbar = not args.inhibit_progress_bar and not args.silent \
        and sys.stderr.isatty()

    if show_pbar:
        try:
            from m_lib.pbar.tty_pbar import ttyProgressBar
        except ImportError:
            show_pbar = False

    if show_pbar:
        try:
            size = os.path.getsize(args.fname1)
        except Exception:
            print(args.fname1, ": no such file")
            sys.exit(1)

    if show_pbar:
        pbar = ttyProgressBar(0, size)

    file1 = open(args.fname1, 'rb')
    file2 = open(args.fname2, 'rb')

    M = 1024*1024
    diff = False
    count = 0

    while True:
        block1 = file1.read(M)
        block2 = file2.read(M)

        if show_pbar:
            pbar.display(file1.tell())

        if block1 and block2:
            if len(block1) != len(block2):
                report(args.silent)
                break
        elif block1:
            report(args.silent)
            break
        elif block2:
            report(args.silent)
            break
        else:
            break

        if block1 != block2:
            report(args.silent)
            break

        count += 1

    if show_pbar and not diff:
        del pbar

    file1.close()
    file2.close()

    if diff:
        sys.exit(1)
