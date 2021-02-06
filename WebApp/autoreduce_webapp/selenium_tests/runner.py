# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
"""
Test runner script for selenium tests
"""
import argparse
import sys

import pytest

from utils.project.structure import get_project_root
from selenium_tests import configuration
from selenium_tests.configuration import store_original_config


def main():
    """
    Main function for selenium test runner
    """
    store_original_config()
    parser = argparse.ArgumentParser(description="Selenium tests for autoreduction WebApp")
    parser.add_argument("-u", "--url", metavar="<url>",
                        help="target url to run tests against. Default is localhost:8000."
                             " Note if you are passing an ip address, it must still be prefixed"
                             " with 'https://'")
    parser.add_argument("-v", "--verbose", dest="verbosity", action="store_const", const=2,
                        default=1, help="Show the verbose test output")
    parser.add_argument("-q", "--quiet", dest="verbosity", action="store_const", const=0,
                        default=1, help="Show the quiet test output")
    parser.add_argument("--headless", dest="is_headless", action="store_const", const=True,
                        default=False, help="Run the tests with headless browser")
    parser.add_argument("-n", "--numcpu", metavar="<Number of CPUs to use>", dest="cpu", default=2)
    args = parser.parse_args()

    if args.url:
        configuration.set_url(args.url)
    if args.is_headless:
        configuration.set_headless(True)


    exit_code = pytest.main([get_project_root() + "/webtests/tests", f"-n{args.cpu}", "-v",
                                 "--ds=autoreduce_webapp.settings"])
    configuration.cleanup_config()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()