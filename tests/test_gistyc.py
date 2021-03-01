"""Testing suite for the gistyc functionalities."""

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
AUTH_TOKEN = os.environ['GIST_TOKEN']


def test_gistyc_create_n_delete_id():
    """
    Testing the creation and deletion of a GIST by a GIST ID.

    Returns
    -------
    None.

    """

    # Initiate the GISTyc class with the auth token
    gist_api = gistyc.GISTyc(auth_token=AUTH_TOKEN)

    # Create a GIST with the sample file
    response_data = gist_api.create_gist(file_name=USAMPLE_FILE_PATH)

    # Check whether the creation was successful by considering the response from GitHub
    assert 'sample.py' in response_data['files'].keys()

    # Delete the GIST, based on the reponse's ID and check for the status code 204
    response_data = gist_api.delete_gist(gist_id=response_data['id'])
    assert response_data == 204


def test_gistyc_create_n_delete_filename():
    """
    Testing the creation and deletion of a GIST by the file name.

    Returns
    -------
    None.

    """

    # Initiate the GISTyc class with the auth token
    gist_api = gistyc.GISTyc(auth_token=AUTH_TOKEN)

    # Create a GIST with the sample file
    response_data = gist_api.create_gist(file_name=USAMPLE_FILE_PATH)

    # Check whether the creation was successful by considering the response from GitHub
    assert 'sample.py' in response_data['files'].keys()

    # Delete the GIST, based on the reponse's ID and check for the status code 204
    response_data = gist_api.delete_gist(file_name='sample.py')
    assert response_data == 204


def test_gistyc_create_n_update():
    """
    Testing the creation and update of a GIST. Afterwards the GIST is deleted. The update is purely
    based on the test file name.

    Returns
    -------
    None.

    """

    # Initiate the GISTyc class with the auth token
    gist_api = gistyc.GISTyc(auth_token=AUTH_TOKEN)

    # Create a GIST
    _ = gist_api.create_gist(file_name=USAMPLE_FILE_PATH)

    # Wait a second
    time.sleep(1)

    # Update the GIST with the updated sample file (update is based on the file's name)
    response_update_data = gist_api.update_gist(file_name=USAMPLE_FILE_PATH)

    # Check whether the update date time is larger, respectively "more recent" than the creation
    # date time
    assert response_update_data['updated_at'] > response_update_data['created_at']

    # Delete the GIST, based on the reponse's ID and check for the status code 204
    response_data = gist_api.delete_gist(gist_id=response_update_data['id'])
    assert response_data == 204


def test_gistyc_create_n_update_id():
    """
    Testing the creation, update and deletion of a GIST. The update is based on the GIST ID.

    Returns
    -------
    None.

    """

    # Initiate the GISTyc class with the auth token
    gist_api = gistyc.GISTyc(auth_token=AUTH_TOKEN)

    # Create the GIST
    response_create_data = gist_api.create_gist(file_name=CSAMPLE_FILE_PATH)

    # Wait for a second
    time.sleep(1)

    # Update the GIST based on the GISTs ID
    response_update_data = gist_api.update_gist(file_name=USAMPLE_FILE_PATH,
                                                gist_id=response_create_data['id'])

    # Check whether the update date time is larger, respectively "more recent" than the creation
    # date time
    assert response_update_data['updated_at'] > response_update_data['created_at']

    # Delete the GIST, based on the reponse's ID and check for the status code 204
    response_data = gist_api.delete_gist(gist_id=response_update_data['id'])
    assert response_data == 204


@pytest.mark.xfail(raises=gistyc.GISTAmbiguityError)
def test_gistyc_ambiguous():
    """
    Testing the custom exception GISTAmbiguityError. If only a filename is provided, but to GISTs
    are present with the same file name an update cannot be performed.

    Returns
    -------
    None.

    """

    # Initiate the GISTyc class with the auth token
    gist_api = gistyc.GISTyc(auth_token=AUTH_TOKEN)

    # Create a GIST with the creation sample file
    _ = gist_api.create_gist(file_name=CSAMPLE_FILE_PATH)

    # Create a second GIST with the same creation sample file
    _ = gist_api.create_gist(file_name=CSAMPLE_FILE_PATH)

    # Now, the update should not succeed, since the update is not based on a GIST ID, but a file
    # name. Since two GISTs have the same name (but different IDs) the test should fail.
    _ = gist_api.update_gist(file_name=USAMPLE_FILE_PATH)


def test_gistyc_clean_ambiguous():
    """
    Testing the method that gets all GISTs from all pages. Afterwards, all files are deleted that
    correspond to the example file.

    Returns
    -------
    None.

    """

    # Initiate the GISTyc class with the auth token
    gist_api = gistyc.GISTyc(auth_token=AUTH_TOKEN)

    # Get a list of all GISTs
    response_gists_list = gist_api.get_gists()

    # Iterate through all GISTs
    for k in response_gists_list:

        # If the sample file name is present in a GIST, get the ID and delete the GIST. Check for
        # the status code 204
        if CSAMPLE_FILE_NAME in k['files']:
            response_data = gist_api.delete_gist(gist_id=k['id'])
            assert response_data == 204
