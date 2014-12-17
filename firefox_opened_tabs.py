#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import html
import json
import os
import platform
import sys


# some constants
FF_PATHS = {
    'Darwin': "Library/Application Support/Firefox/Profiles",
    'Linux': ".mozilla/firefox/",
    'Windows': "AppData\Roaming\Mozilla\Firefox\Profiles"
}
FF_DIR = os.path.join(os.environ['HOME'], FF_PATHS[platform.system()])
POSSIBLE_SESSION_FILES = [
    "sessionstore.js",
    os.path.join("sessionstore-backups", "recovery.js"),
    os.path.join("sessionstore-backups", "recovery.bak"),
    os.path.join("sessionstore-backups", "previous.js"),
]
PREFIX = '_FOT_'
FOT_HTML = "firefox_opened_tabs.html"


def find_ff_sessionstore():
    """ Find the right file to parse. """
    if not os.path.isdir(FF_DIR):
        sys.exit("ERROR: can't find your main Firefox directory :-(")

    session_file = None
    profile_dir = None
    files = os.listdir(FF_DIR)
    for f in files:
        if os.path.isdir(os.path.join(FF_DIR, f)) and '.' in f:
            found = False
            for possible_session_file in POSSIBLE_SESSION_FILES:
                if os.path.isfile(os.path.join(FF_DIR, f, possible_session_file)):
                    profile_dir = os.path.join(FF_DIR, f)
                    session_file = possible_session_file
                    found = True
                    print("INFO: your Firefox profile directory is " + profile_dir)
                    break
                else:
                    print("WARN: can't find session file {}".format(possible_session_file))
    if not found:
        sys.exit("ERROR: can't find any session file")
    return(os.path.join(profile_dir, session_file))


def extract_urls(sessionstore):
    """ Parse the sessionstore file to extract urls. """
    ungrouped_urls = []
    pinned_urls = []
    url_dict = {}

    with open(sessionstore) as f:
        window = None
        try:
            window = json.loads(f.read()).get("windows")[0]
        except ValueError:
            sys.exit("ERROR: can't read the given file :-(")
        # find groups of tabs
        groups = None
        nb_group = 0
        if 'extData' in window and 'tabview-group' in window['extData']:
            groups = json.loads(window['extData']['tabview-group'])
            nb_group = len(groups)
            for group in groups:
                url_dict[PREFIX + groups[group]['title']] = []

        print("INFO: you have {} tabs in {} groups".format(len(window['tabs']),
                                                           nb_group))

        if 'tabs' in window:
            for tab in window['tabs']:
                if 'entries' in tab:
                    # the last one in history is the one currently displayed
                    entry = tab['entries'][-1]
                    url = entry['url']
                    title = url
                    if 'title' in entry:
                        title = tab['entries'][-1]['title']
                    li_dict = {'url': url, 'title': title}

                    # first possible case, the tab is pinned
                    if 'pinned' in tab and tab['pinned'] is True:
                        pinned_urls.append(li_dict)
                    # or is the tab in a group? (FF's Panorama feature)
                    elif 'extData' in tab and 'tabview-tab' in tab['extData']:
                        tabview = json.loads(tab['extData']['tabview-tab'])
                        if 'groupID' in tabview:
                            group_id = str(tabview['groupID'])
                            if group_id and group_id in groups:
                                group = PREFIX + groups[group_id]['title']
                                url_dict[group].append(li_dict)
                    else:
                        ungrouped_urls.append(li_dict)

    # create dictionaries of urls
    if pinned_urls:
        url_dict['pinned'] = pinned_urls
    if ungrouped_urls:
        url_dict['ungrouped_urls'] = ungrouped_urls

    return(url_dict)


def generate_ul(url_list):
    ul = '<ul>'
    for li_dict in url_list:
        url = html.escape(li_dict['url'])
        title = html.escape(li_dict['title'])
        ul += '<li><a href="{u}">{t}</a></li>'.format(u=url, t=title)
    ul += '</ul>'
    return(ul)


def generate_output(url_dict):
    """ Generate a HTML page with the list of urls. """
    content = ''

    if 'pinned' in url_dict:
        content += '<h2>Pinned tabs</h2>'
        content += generate_ul(url_dict['pinned'])
        url_dict.pop('pinned', None)

    if 'ungrouped_urls' in url_dict:
        content += '<h2>All other tabs</h2>'
        content += generate_ul(url_dict['ungrouped_urls'])
        url_dict.pop('ungrouped_urls', None)

    for key in sorted(url_dict.keys()):
        if url_dict[key]:
            title = key.replace(PREFIX, '')
            if not title:
                title = 'Unnamed group'
            content += '<h2>{}</h2>'.format(title)
            content += generate_ul(url_dict[key])

    return("""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>
        {content}
    </body>
    </html>
    """.format(content=content, title='Your Firefox opened tabs'))


def write_file(content):
    with open(FOT_HTML, "w") as output:
        output.write(content)
    print("INFO: list of opened tabs successfully written!")


def main(argv):
    sessionstore = None
    if len(argv) == 2 and os.path.isfile(argv[1]):
        sessionstore = argv[1]
    else:
        sessionstore = find_ff_sessionstore()
    urls = extract_urls(sessionstore)
    output = generate_output(urls)
    write_file(output)


if __name__ == '__main__':
    main(sys.argv)
