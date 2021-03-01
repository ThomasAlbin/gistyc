"""Testing routine for the GISTyc CLI"""

# Import standard libraries
import ast
import os
import time

# Import installed libraries
from click.testing import CliRunner

# Import GISTyc
import gistyc

# First, set the file name paths to the sample.py for creating and update the GISTs.
CORE_PATH = os.path.dirname(os.path.abspath(__file__))

CSAMPLE_FILE_NAME = 'sample.py'
CSAMPLE_FILE_PATH = os.path.join(CORE_PATH, '_resources/create', CSAMPLE_FILE_NAME)

USAMPLE_FILE_NAME = 'sample.py'
USAMPLE_FILE_PATH = os.path.join(CORE_PATH, '_resources/update', USAMPLE_FILE_NAME)

# Get the GIST authentication token from the system environment
AUTH_TOKEN = os.environ['GIST_TOKEN']


def test_cli_create_n_delete_id():
    """Testing the creation and deletion of a GIST, based on the ID.

    Returns
    -------
    None.

    """

    # Set up the CLI Runner and execute the create command
    runner = CliRunner()
    cresult = runner.invoke(gistyc.cli.run, ['--create',
                                             '--auth-token', AUTH_TOKEN,
                                             '--file-name', CSAMPLE_FILE_PATH])

    # Check if the CLI ran error free
    assert cresult.exit_code == 0

    # Convert the response to JSON by identifying the format automatically
    cresult_data = ast.literal_eval(cresult.output)

    # Check if the file name is in the GIST REST API response
    assert CSAMPLE_FILE_NAME in cresult_data['files'].keys()

    # Set up the CLI Runner and execute the delete command
    runner = CliRunner()
    dresult = runner.invoke(gistyc.cli.run, ['--delete',
                                             '--auth-token', AUTH_TOKEN,
                                             '--gist-id', cresult_data['id']])

    # Check if the CLI ran error free
    assert dresult.exit_code == 0

    # Check the HTTP status code
    assert '204' in dresult.output


def test_cli_create_n_delete():
    """Testing the creation and deletion of a GIST, based on the file name.

    Returns
    -------
    None.

    """

    # Set up the CLI Runner and execute the create command
    runner = CliRunner()
    cresult = runner.invoke(gistyc.cli.run, ['--create',
                                             '--auth-token', AUTH_TOKEN,
                                             '--file-name', CSAMPLE_FILE_PATH])

    # Check if the CLI ran error free
    assert cresult.exit_code == 0

    # Convert the response to JSON by identifying the format automatically
    cresult_data = ast.literal_eval(cresult.output)

    # Check if the file name is in the GIST REST API response
    assert CSAMPLE_FILE_NAME in cresult_data['files'].keys()

    # Set up the CLI Runner and execute the delete command
    runner = CliRunner()
    dresult = runner.invoke(gistyc.cli.run, ['--delete',
                                             '--auth-token', AUTH_TOKEN,
                                             '--file-name', CSAMPLE_FILE_PATH])

    # Check if the CLI ran error free
    assert dresult.exit_code == 0

    # Check the HTTP status code
    assert '204' in dresult.output


def test_cli_create_n_update_file():
    """Testing the creation and update of a GIST (based on the pure file name).

    Returns
    -------
    None.

    """

    # Set up the CLI Runner and execute the create command
    runner = CliRunner()
    cresult = runner.invoke(gistyc.cli.run, ['--create',
                                             '--auth-token', AUTH_TOKEN,
                                             '--file-name', CSAMPLE_FILE_PATH])

    # Check if the CLI ran error free
    assert cresult.exit_code == 0

    # Convert the response to JSON by identifying the format automatically
    cresult_data = ast.literal_eval(cresult.output)

    # Check if the file name is in the GIST REST API response
    assert CSAMPLE_FILE_NAME in cresult_data['files'].keys()

    # Wait for a second, to clearly set a difference between the creation and update datetime
    time.sleep(1)

    # Set up the CLI Runner and execute the update command
    runner = CliRunner()
    uresult = runner.invoke(gistyc.cli.run, ['--update',
                                             '--auth-token', AUTH_TOKEN,
                                             '--file-name', USAMPLE_FILE_PATH])

    # Check if the CLI ran error free
    assert uresult.exit_code == 0

    # Convert the response to JSON by identifying the format automatically
    uresult_data = ast.literal_eval(uresult.output)

    # Check if the create date time is older than the update datetime
    assert uresult_data['updated_at'] > uresult_data['created_at']

    # Set up the CLI Runner and execute the delete command
    dresult = runner.invoke(gistyc.cli.run, ['--delete',
                                             '--auth-token', AUTH_TOKEN,
                                             '--gist-id', uresult_data['id']])
    # Check if the CLI ran error free
    assert dresult.exit_code == 0

    # Check the HTTP status code
    assert '204' in dresult.output

def test_cli_create_n_update_id():
    """Testing the creation and update of a GIST (based on the GIST ID).

    Returns
    -------
    None.

    """

    # Set up the CLI Runner and execute the create command
    runner = CliRunner()
    cresult = runner.invoke(gistyc.cli.run, ['--create',
                                             '--auth-token', AUTH_TOKEN,
                                             '--file-name', CSAMPLE_FILE_PATH])
    # Check if the CLI ran error free
    assert cresult.exit_code == 0

    # Convert the response to JSON by identifying the format automatically
    cresult_data = ast.literal_eval(cresult.output)

    # Check if the file name is in the GIST REST API response
    assert CSAMPLE_FILE_NAME in cresult_data['files'].keys()

    # Wait for a second, to clearly set a difference between the creation and update datetime
    time.sleep(1)

    # Set up the CLI Runner and execute the update command
    runner = CliRunner()
    uresult = runner.invoke(gistyc.cli.run, ['--update',
                                             '--auth-token', AUTH_TOKEN,
                                             '--file-name', USAMPLE_FILE_PATH,
                                             '--gist-id', cresult_data['id']])

    # Check if the CLI ran error free
    assert uresult.exit_code == 0

    # Convert the response to JSON by identifying the format automatically
    uresult_data = ast.literal_eval(uresult.output)

    # Check if the create date time is older than the update datetime
    assert uresult_data['updated_at'] > uresult_data['created_at']

    # Set up the CLI Runner and execute the delete command
    dresult = runner.invoke(gistyc.cli.run, ['--delete',
                                             '--auth-token', AUTH_TOKEN,
                                             '--gist-id', uresult_data['id']])
    # Check if the CLI ran error free
    assert dresult.exit_code == 0

    # Check the HTTP status code
    assert '204' in dresult.output
