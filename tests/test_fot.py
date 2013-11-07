# -*- coding: utf-8 -*-
""" Test suite for the models.py file. """

# system
import os
import sys
# nose
from nose.tools import raises
#from nose.tools import assert_equal
#from nose.tools import assert_not_equal
#from nose.tools import nottest
# local
import firefox_opened_tabs


@raises(SystemExit)
def test_fixture_not_a_session_file():
    """ Giving a not-JSON-session-file to the script. """
    sessionstore = os.path.abspath(__file__)
    argv = ['firefox_opened_tabs.py', sessionstore]
    firefox_opened_tabs.main(argv)
