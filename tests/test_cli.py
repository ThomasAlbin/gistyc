"""TBW"""

# Import standard libraries
import os
import time

# Import installed libraries
import pytest

# Import GISTyc
import gistyc

from click.testing import CliRunner

import json
import ast

# First, set the file name paths to the sample.py for creating and update the GISTs.
CORE_PATH = os.path.dirname(os.path.abspath(__file__))

CSAMPLE_FILE_NAME = 'sample.py'
CSAMPLE_FILE_PATH = os.path.join(CORE_PATH, '_resources/create', CSAMPLE_FILE_NAME)

USAMPLE_FILE_NAME = 'sample.py'
USAMPLE_FILE_PATH = os.path.join(CORE_PATH, '_resources/update', USAMPLE_FILE_NAME)

# Get the GIST authentication token from the system environment
AUTH_TOKEN = os.environ['gist_token']


def test_cli_create_n_delete():
    """
    Testing the creation and deletion of a GIST.

    Returns
    -------
    None.

    """

    runner = CliRunner()
    cresult = runner.invoke(gistyc.cli.run, ['--create', 
                                             '--auth-token', AUTH_TOKEN,
                                             '--file-name', CSAMPLE_FILE_PATH])
    assert cresult.exit_code == 0
    cresult_data = ast.literal_eval(cresult.output)
    assert CSAMPLE_FILE_NAME in cresult_data['files'].keys()

    time.sleep(1)

    runner = CliRunner()
    dresult = runner.invoke(gistyc.cli.run, ['--delete', 
                                             '--auth-token', AUTH_TOKEN,
                                             '--gist-id', cresult_data['id']])
    assert dresult.exit_code == 0
    assert '204' in dresult.output

def test_cli_create_n_update_file():

    runner = CliRunner()
    cresult = runner.invoke(gistyc.cli.run, ['--create', 
                                             '--auth-token', AUTH_TOKEN,
                                             '--file-name', CSAMPLE_FILE_PATH])
    assert cresult.exit_code == 0
    cresult_data = ast.literal_eval(cresult.output)
    assert CSAMPLE_FILE_NAME in cresult_data['files'].keys()

    runner = CliRunner()
    uresult = runner.invoke(gistyc.cli.run, ['--update', 
                                             '--auth-token', AUTH_TOKEN,
                                             '--file-name', USAMPLE_FILE_PATH])
    assert uresult.exit_code == 0
    uresult_data = ast.literal_eval(uresult.output)
    assert uresult_data['updated_at'] > uresult_data['created_at']


    dresult = runner.invoke(gistyc.cli.run, ['--delete', 
                                             '--auth-token', AUTH_TOKEN,
                                             '--gist-id', uresult_data['id']])
    assert dresult.exit_code == 0
    assert '204' in dresult.output

def test_cli_create_n_update_id():

    runner = CliRunner()
    cresult = runner.invoke(gistyc.cli.run, ['--create', 
                                             '--auth-token', AUTH_TOKEN,
                                             '--file-name', CSAMPLE_FILE_PATH])
    assert cresult.exit_code == 0
    cresult_data = ast.literal_eval(cresult.output)
    assert CSAMPLE_FILE_NAME in cresult_data['files'].keys()

    runner = CliRunner()
    uresult = runner.invoke(gistyc.cli.run, ['--update', 
                                             '--auth-token', AUTH_TOKEN,
                                             '--file-name', USAMPLE_FILE_PATH,
                                             '--gist-id', cresult_data['id']])
    assert uresult.exit_code == 0
    uresult_data = ast.literal_eval(uresult.output)
    assert uresult_data['updated_at'] > uresult_data['created_at']


    dresult = runner.invoke(gistyc.cli.run, ['--delete', 
                                             '--auth-token', AUTH_TOKEN,
                                             '--gist-id', uresult_data['id']])
    assert dresult.exit_code == 0
    assert '204' in dresult.output