#! /usr/bin/env python

import subprocess
import sys
from ppu_tu import setup, teardown, find_in_path  # noqa


test_prog_path = find_in_path('which.py')


def test_which():
    assert subprocess.check_output(
        [sys.executable, test_prog_path, "which.py"],
        universal_newlines=True).strip() == test_prog_path
    assert subprocess.check_output(
        [sys.executable, test_prog_path, "WhoWhereWhenceWhichWhereIs.py"],
        universal_newlines=True).strip() == ''
