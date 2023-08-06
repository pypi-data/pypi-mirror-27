#!/usr/bin/env python

import sys

from gpxconverter.converter import convert


def main():
    convert(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
