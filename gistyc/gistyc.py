"""Main GISTys script that contains all required parts of the module."""

# Import standard libraries
import json
from pathlib import Path
import requests


class GISTAmbiguityError(Exception):
    """TBW"""
    def __init__(self, gist_ids_list, message="Number of GIST IDs is too ambiguous"):
        """Initiate the Exception class

        Parameters
        ----------
        gist_ids_list : list
            List of strings with GIST IDs.
        message : str, optional
            Default exception message. The default is "Number of GIST IDs is too ambiguous".

        Returns
        -------
        None.

        """

        # Set the instances; list of GIST IDs and message
        self.gist_ids_list = gist_ids_list
        self.message = message

        # Super call itself to create message
        super().__init__(self.message)


    def __str__(self):
        """Modifying the message function

        Returns
        -------
        str
            Exception message.

        """

        return f'{self.message}\nIDs: ' + ', '.join(self.gist_ids_list)


class GISTyc:
    """This class is used to access the GitHub GIST REST API functions to create, update and delete
    GISTs.

    The advantage of this class and its corresponding methods is the capability to update
    e.g., already existing GISTs (with multiple files) that are e.g., embedded in an online
    tutorial. Updateing GISTs automatically is useful if the GISTs corresponding online
    documentation is not valid anymore. Updating GISTs manually is tedious and erorr-prone.
    However, integrating GISTyc in a CI/CD pipeline (via GitHub Actions) may improve the
    maintainability of already exisiting GIST codes.

    """


    def __init__(self, auth_token):
        """Initiate the GISTys class with the GitHub GIST REST API token

        Parameters
        ----------
        auth_token : str
            Authentication token of the GitHub GIST REST API.

        Returns
        -------
        None.

        """

        # Set the authentication token
        self.auth_token = auth_token

        # Set the default header for the REST API
        self._headers = {'Authorization': f'token {auth_token}'}


    @staticmethod
    def _readnparse_python_file(file_name):
        """Helper function within the class to read a Python file and return a REST API - ready
        body.

        Parameters
        ----------
        file_name : pathlib.Path or str
            Absolute or relative path name of the file to read.

        Returns
        -------
        data : dict
            Body for the REST API call.

        """

        # Set the filename as a Path
        file_name = Path(file_name)

        # Open the file and read the content. The entire content is stored in a single string.
        with open(file_name, 'r') as file_obj:
            file_content = file_obj.read()

        # Get the file name without the path
        core_file_name = file_name.name

        # Split the python file content at the cell separator "#%%". The resulting list contains
        # the code blocks as individual array elements
        file_content = file_content.split('#%%')

        # The python code (blocks) must be put into a dictionary that is later used as a JSON
        # in the request REST API body
        gist_code_dict = {}

        # Iterate through the list of code blocks
        for index, k in enumerate(file_content):

            # At the first index, simply add the content with the original file name ...
            if index == 0:
                gist_code_dict[core_file_name] = {"content": k}

            # ... all other GIST file names get a consecutive, index depending number as a suffix
            else:
                gist_code_dict[core_file_name.replace('.py', f'_{index}.py')] = {"content": k}

        # Put the content in a dictionary for the REST API
        data = {"public" : True, "files" : gist_code_dict, }

        return data


    def get_gists(self):
        """Get all GISTs information (ID, url, meta information, etc.)

        Returns
        -------
        resp_data : list
            List of GISTs. Each GIST is a dictionary with miscellaneous data and meta data.

        """

        # Set the REST API url to obtain the list of GISTs. PAGE will be replace later in a loop.
        # Per page: a max. value of 100 GISTs is requested
        _query_url = "https://api.github.com/gists?page=PAGE&per_page=100"

        # All GISTs shall be stored in this placeholder array
        resp_data = []

        # To iterate through the GIST pages, set an inital counter that will incrementally increase
        cntr = 0

        # While condition: Iterate trough the GIST pages, until the response is empty
        _resp_ansr = True
        while _resp_ansr:
            cntr += 1

            # Get the GISTs for a particular page
            resp = requests.get(_query_url.replace('PAGE', str(cntr)), headers=self._headers)
            resp_content = resp.json()

            # If the response is not empty, obtain the results and extend the placeholder array
            if len(resp_content) > 0:
                resp_data.extend(resp_content)

            # Otherwise set the while condition to false
            else:
                _resp_ansr = False

        return resp_data


    def create_gist(self, file_name):
        """Create a GISTs from a given file. Use "#%%" as a block separator to create sub-GISTs /
        files from a single input file

        Parameters
        ----------
        file_name : pathlib.Path or str
            Absolute or relative path name of the file to read.

        Returns
        -------
        resp_data : dict
            GIST REST API response.

        """

        # Set the REST API url for creating a GIST
        _query_url = "https://api.github.com/gists"

        # Read the file and return the body for the REST API call
        rest_api_data = self._readnparse_python_file(file_name)

        # Call the REST API and obtain the response
        resp = requests.post(_query_url, headers=self._headers, data=json.dumps(rest_api_data))
        resp_data = resp.json()

        return resp_data


    def update_gist(self, file_name, gist_id=None):
        """Update a GISTs based on its file name or GIST ID. If the file name is provided it is
        assumed that only one GIST corresponds to the input's file name.

        Parameters
        ----------
        file_name : pathlib.Path or str
            Absolute or relative path name of the file to read.
        gist_id : str, optional
            GIST ID that is needed if the file name appears more than once in the GIST repository.
            The default is None.

        Raises
        ------
        GISTAmbiguityError
            If several GISTs have the same file name, but no GIST ID is provided as an input this
            exception is raised.

        Returns
        -------
        resp_data : dict
            GIST REST API response.

        """

        # Convert the file name to pathlib.Path
        file_name = Path(file_name)

        # Iterate trough all gists and append all IDs that contain the file name (if requested!)
        gist_ids = []
        if not gist_id:

            # Get all GISTs
            gist_list = self.get_gists()

            # Iterate trough all GISTs
            for _gist in gist_list:

                # Check if the file name is present in the GIST
                if file_name.name in _gist['files']:

                    # Append the corresponding GIST
                    gist_ids.append(_gist['id'])

            # Take only the first entry as the GIST ID of interest. There should only be 1 ID
            # present
            gist_id = gist_ids[0]

        # If more than 1 GIST ID is present: raise an exception
        if len(gist_ids) > 1:
            raise GISTAmbiguityError(gist_ids_list=gist_ids)

        # Set the REST API url to update a GIST
        _query_url = f'https://api.github.com/gists/{gist_id}'

        # Read and parse the file
        rest_api_data = self._readnparse_python_file(file_name)

        # Update the GIST and get the response
        resp = requests.patch(_query_url, headers=self._headers, data=json.dumps(rest_api_data))
        resp_data = resp.json()

        return resp_data


    def delete_gist(self, gist_id):
        """Delete a GIST based on its GIST ID.

        Parameters
        ----------
        gist_id : str
            GIST ID to delete.

        Returns
        -------
        resp_status : int
            HTTP response code. A successful deletion shall return 204.

        """

        # Set the REST API url for deleting a GIST
        _query_url = f'https://api.github.com/gists/{gist_id}'

        # Delete the GIST and get the status code from the response
        resp = requests.delete(_query_url, headers=self._headers)
        resp_status = resp.status_code

        return resp_status
