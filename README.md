[![Build Status](https://travis-ci.org/stephanepechard/firefox_opened_tabs.png?branch=master)](https://travis-ci.org/stephanepechard/firefox_opened_tabs)
[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/stephanepechard/firefox_opened_tabs/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

Firefox opened tabs script
==========================

A small Python3 script to extract opened tabs from Firefox.
Should work on Linux, Mac OS X and Windows systems with Python >= 3.2.


Basic usage
-----------

    python3 firefox_opened_tabs.py

will create, in the same directory, a `firefox_opened_tabs.html` file containing
the list of all opened tabs in your Firefox. The script tries to find
your Firefox profile's directory the best as it can. Tabs are grouped as they
are in your Firefox.

With a specified file
---------------------

You can also specified a file to be parsed by `firefox_opened_tabs` instead
of the one of your profile with:

    python3 firefox_opened_tabs.py /home/user/the_file.js


About
=====

Made with love and Debian by Stéphane Péchard. Feel free to contribute,
criticize and tell me what you think about it!
