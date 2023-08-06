# -*- coding: utf-8 -*-
'''
casperjs cli script runner & reader. Downloads any urls sent to stdout from the specified casperjs script
'''

import argparse
import re
import os
from os import path
from distutils import spawn
import subprocess as sp

import requests


url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def parse_script_output(params):
    print u'calling {0}'.format(params)
    #child = sp.Popen(''.join(params), shell=True, stderr=sp.PIPE)
    out = sp.check_output(params)
    return [url for url in out.split() if url_regex.match(url)]
 
def download_file(url):
    resp = requests.get(url, stream=True)
    filename = None
    if 'Content-Disposition' in resp.headers:
        try:
            filename = re.search(r'filename="([\w\s\-\.]*)"', resp.headers['Content-Disposition']).group(1)
        except:
            print u'No filename found in Content-Disposition header: {0}'.format(resp.headers['Content-Disposition'])
    if not filename:
        end = len(url) if url.rfind('?', url.rfind('/')) < 0 else url.rfind('?', url.rfind('/'))
        filename = url[url.rfind('/'):end]
    with open(filename, 'wb') as fout:
        for chunk in resp.iter_content(chunk_size=1024):
            fout.write(chunk)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a casperjs script and possibly some urls')
    parser.add_argument('script', metavar='script', type=str, nargs=1, help='a casperjs script to run')
    parser.add_argument('-u', '--url', dest='urls', type=str, nargs='*', help='one or more urls for the script to be run against sequentially')
    parser.add_argument('-c', '--casperjs', dest='casperjs', type=str, nargs='?', help='optional path to casperjs')

    args = parser.parse_args()

    script = args.script[0]
    urls = []
    if args.urls:
        urls = args.urls
    casper = ''
    if args.casperjs:
        casper = args.casperjs

    good_urls = []
    for url in urls:
        if not url_regex.match(url):
            print u'bad url parameter: {0}, ignoring'.format(url)
        else:
            good_urls.append(url)

    # check PHANTOMJS_EXECUTABLE envvar set or phantomjs is on the PATH
    if 'PHANTOMJS_EXECUTABLE' not in os.environ and not spawn.find_executable('phantomjs'):
        print u'phantomjs is not on the PATH nor is PHANTOMJS_EXECUTABLE set, exiting'
        exit()

    if not spawn.find_executable('casperjs') and not casper:
        print u'casperjs is not on the PATH nor is casperjs location provided, exiting'
        exit()

    APP_ROOT = path.dirname(os.path.realpath(__file__))
    if urls:
        for url in urls:
            params =[casper+'/casperjs', script, url]
            for url in parse_script_output(params):
                print u'downloading {0}'.format(url)
                download_file(url)
    else:
        params = [casper+'/casperjs', script]
        for url in parse_script_output(params):
            print u'downloading {0}'.format(url)
            download_file(url)
  