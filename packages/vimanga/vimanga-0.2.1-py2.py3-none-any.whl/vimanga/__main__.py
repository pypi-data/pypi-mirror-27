#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main module."""
import fire
from vimanga.cli import find


class ViManga(object):
    """Parse object run cli mode"""
    def __init__(self, *args, **kwargs):
        self.find = find


def main():
    """Entry point"""
    fire.Fire(ViManga())


if __name__ == '__main__':
    main()
