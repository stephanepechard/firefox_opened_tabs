Firefox opened tabs script
==========================

A small Python3 script to extract opened tabs from Firefox.
Should work on any UNIX-based systems.


Usage
-----

    python3 firefox_opened_tabs.py

will create, in the same directory, a `firefox_opened_tabs.html` file containing
the list of all opened tabs in your Firefox. The script tries to find
your Firefox profile's directory the best as it can.

You can't do much more right now. Next step would be to group your tabs
in the generated file as they are in Firefox.
