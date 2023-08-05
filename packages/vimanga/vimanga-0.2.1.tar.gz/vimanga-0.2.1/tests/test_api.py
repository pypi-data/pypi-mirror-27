#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `vimanga` package."""

import pytest

from vimanga.api.core import call_api, get_chapters, get_images
from vimanga.api.types import Manga, Chapters


@pytest.fixture
def manga():
    """Manga Sample"""
    return Manga(21937, 'type', 'score', 'name', 'synopsis', 'genders')


@pytest.fixture
def chapters(manga):
    """Chapters of manga"""
    return next(get_chapters(manga))


def test_api_works():
    """Test not change the api"""
    resp = call_api()

    assert resp.ok, 'Problem with page message={}'.format(resp.text)


def test_get_sample_manga(manga, chapters):
    """Test with a sample manga"""
    total = chapters.total
    _chapters = chapters.data

    message = 'Problem with manga id {} {} not is {}'
    assert total == 6, message.format(manga.id, 'total', 6)

    assert _chapters, 'Not fetch chapters'


def test_get_sample_images(chapters: Chapters):
    """Test with a sample cap"""
    chapter = chapters.data[0]
    resp = list(get_images(chapter))

    assert isinstance(resp, list)
    assert len(resp) > 6
