# -*- coding: utf-8 -*-
""" Test suite for the models.py file. """

# system
from io import StringIO
import os
import sys
# nose
import nose
from nose.plugins.capture import Capture
from nose.plugins.manager import PluginManager
from nose.tools import raises
#from nose.tools import assert_equal
#from nose.tools import assert_not_equal
from nose.tools import nottest
# local
import firefox_opened_tabs


@raises(SystemExit)
def test_fixture_not_a_session_file():
    """ Giving a not-JSON-session-file to the script. """
    argv = ['firefox_opened_tabs.py', os.path.abspath(__file__)]
    firefox_opened_tabs.main(argv)


def assert_output(test_func, expected_output):

    saved_stdout = sys.stdout
    try:
        out = StringIO()
        sys.stdout = out

        test_func()

        output = out.getvalue().strip()
        assert output == expected_output
    finally:
        sys.stdout = saved_stdout


def test_fixture_ok():
    """ Legitimate use with a newly created session file. """

    def fixture_ok():
        argv = ['firefox_opened_tabs.py', 'tests/sessionstore.js']
        firefox_opened_tabs.main(argv)

    expected_output = 'INFO: you have 2 tabs in 0 groups\nINFO: list of opened tabs successfully written!'

    assert_output(fixture_ok, expected_output)

