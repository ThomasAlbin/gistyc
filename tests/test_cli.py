"""TBW"""

# Import standard libraries
import os
import time

# Import installed libraries
import pytest

# Import GISTyc
import gistyc

# First, set the file name paths to the sample.py for creating and update the GISTs.
CORE_PATH = os.path.dirname(os.path.abspath(__file__))

CSAMPLE_FILE_NAME = 'sample.py'
CSAMPLE_FILE_PATH = os.path.join(CORE_PATH, '_resources/create', CSAMPLE_FILE_NAME)

USAMPLE_FILE_NAME = 'sample.py'
USAMPLE_FILE_PATH = os.path.join(CORE_PATH, '_resources/update', USAMPLE_FILE_NAME)

# Get the GIST authentication token from the system environment
AUTH_TOKEN = os.environ['gist_token']


def test_gistyc_create_n_delete():
    """
    Testing the creation and deletion of a GIST.

    Returns
    -------
    None.

    """

    gistyc.cli.main()