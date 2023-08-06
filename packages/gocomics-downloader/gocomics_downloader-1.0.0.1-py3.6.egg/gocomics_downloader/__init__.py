#!/usr/bin/env python
# -*- coding: utf-8 -*-

# compatibility
from __future__ import absolute_import, print_function, unicode_literals
from .exceptions import (DoubleInputException, NoInputException, IncompleteInputException

from .downloader import download_file

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2



import bs4
import datetime


def datetime_parser(dt):
    """
    :rtype: list
    :param dt: datetime.datetime object
    :return: the year, month and date
    """
    return dt.strftime('%Y:%m:%d').split(':')


def get_comic_page(comic_name, year=None, month=None, day=None, dt=None):
    """
    :type dt: datetime.datetime
    :type day: int
    :type month: int
    :type year: int
    :type comic_name: str
    :param comic_name: name of the comic
    :param year: the year of the page of the comic, eg 2017
    :param month: the month of the page of the comic, eg 5
    :param day: the day of the page of the comic, eg 26
    :param dt: a datetime.datetime object
    :return: bs4.BeautifulSoup
    """
    if not year is None and not month is None and not day is None:
        ymd = True
    elif year is None and month is None and day is None:
        ymd = False
    else:
        raise exceptions.IncompleteInputException(year, month, day)
    if not dt is None and ymd:
        raise exceptions.DoubleInputException(year, month, day, dt)
    elif not dt is None:
        year, month, day = datetime_parser(dt)
    page = urllib2.urlopen('http://www.gocomics.com/{cn}/{y}/{m}/{d}'.format(cn=comic_name, y=year, m=month,
                                                                             d=day))
    content = page.read()
    soup = bs4.BeautifulSoup(content, "lxml")
    return soup


def process_image(soup):
    findall = soup.find_all('picture', class_='img-fluid item-comic-image')
    entry = findall[0].img['src']
    return entry

def download_image(link, savename = None):
    return download_file(link, dest = savename)
	
def get_picture(comic_name, year = None, month = None, day = None, dt = None, savename = None):
    soup = get_comic_page(comic_name, year = year, month = month, day = day, dt = dt)
    link = process_image(soup)
    download_image(link, savename = savename)

def download_all()
