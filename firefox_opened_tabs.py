#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
from string import Template

# some constants
FF_DIR = os.environ['HOME'] + "/.mozilla/firefox/"
SESSION_FILE = "sessionstore.js"

if not os.path.isdir(FF_DIR):
    sys.exit("ERROR: can't find your main Firefox directory :-(")


def find_ff_sessionstore():
    """ Find the right file to parse. """
    profile_dir = None
    files = os.listdir(FF_DIR)
    for f in files:
        if os.path.isdir(os.path.join(FF_DIR, f)) and '.' in f and \
            os.path.isfile(os.path.join(FF_DIR, f, SESSION_FILE)):
            profile_dir = os.path.join(FF_DIR, f)
            print("INFO: your Firefox profile directory is " + profile_dir)
    return(os.path.join(profile_dir, SESSION_FILE))


def extract_urls(sessionstore):
    """ Parse the sessionstore file to extract urls. """
    tabs_data = None
    url_dict = {}
    urls = []
    pinned_urls = []
    with open(sessionstore) as f:
        tabs_data = json.loads(f.read())
        windows = tabs_data.get("windows")
        for window in windows:
            if 'tabs' in window:
                print("INFO: you have {} tabs".format((len(window['tabs']))))
                for tab in window['tabs']:
                    if 'entries' in tab:
                        # the last one is the one currently displayed
                        url = tab['entries'][-1]['url']
                        if 'pinned' in tab and tab['pinned'] == True:
                            pinned_urls.append(url)
                        else:
                            urls.append(url)

    if pinned_urls:
        url_dict['pinned'] = pinned_urls
    if urls:
        url_dict['urls'] = urls

    return(url_dict)


def generate_ul(url_list):
    ul = '<ul>'
    for url in url_list:
        ul += '<li><a href="{url}">{url}</a></li>'.format(url=url)
    ul += '</ul>'
    return(ul)


def generate_output(url_dict):
    """ Generate a HTML page with the list of urls. """
    content = ''

    if 'pinned' in url_dict:
        content += '<h2>Pinned tabs</h2>'
        content += generate_ul(url_dict['pinned'])

    if 'urls' in url_dict:
        content += '<h2>All other tabs</h2>'
        content += generate_ul(url_dict['urls'])


    template = Template("""<!DOCTYPE html>
    <html lang="en"><head>
        <meta charset="utf-8">
        <title>Generated list of Firefox opened tabs.</title>
    </head><body>
    $content
    </body></html>
    """)

    with open("firefox_opened_tabs.html", "w") as output:
        output.write(template.substitute(content=content))


def main():
    sessionstore = find_ff_sessionstore()
    urls = extract_urls(sessionstore)
    generate_output(urls)


if __name__ == '__main__':
    main()

