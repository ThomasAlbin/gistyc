"""Main GISTys script that contains all required parts of the module."""

# Import standard libraries
import json
from pathlib import Path
import requests


class GISTAmbiguityError(Exception):
    """TBW"""
    def __init__(self, gist_ids_list, message="Number of GIST IDs is too ambiguous"):
        """
        TBW

        Parameters
        ----------
        gist_ids_list : TYPE
            DESCRIPTION.
        message : TYPE, optional
            DESCRIPTION. The default is "Number of GIST IDs is too ambiguous".

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
        """
        TBW

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return f'{self.message}\nIDs: ' + ', '.join(self.gist_ids_list)


class GISTyc:

    def __init__(self, auth_token):

        # Set the authentication token
        self.auth_token = auth_token

        # Set the default header for the REST API
        self._headers = {'Authorization': f'token {auth_token}'}


    @staticmethod
    def _readnparse_python_file(file_name):

        file_name = Path(file_name)

        with open(file_name, 'r') as file_obj:
            file_content = file_obj.read()

        core_file_name = file_name.name

        file_content = file_content.split('#%%')

        gist_code_dict = {}
        for index, k in enumerate(file_content):

            if index == 0:
                gist_code_dict[core_file_name] = {"content": k}

            else:
                gist_code_dict[core_file_name.replace('.py', f'_{index}.py')] = {"content": k}

        data = {"public" : True, "files" : gist_code_dict, }

        return data

    def get_gists(self):

        _query_url = "https://api.github.com/gists?page=PAGE&per_page=100"

        _resp_ansr = True

        resp_data = []

        cntr = 0
        while _resp_ansr:
            cntr += 1

            resp = requests.get(_query_url.replace('PAGE', str(cntr)), headers=self._headers)

            resp_content = resp.json()

            if len(resp_content) > 0:
                resp_data.extend(resp_content)
            else:
                _resp_ansr = False

        return resp_data


    def create_gist(self, file_name):

        _query_url = "https://api.github.com/gists"

        rest_api_data = self._readnparse_python_file(file_name)


        resp = requests.post(_query_url, headers=self._headers, data=json.dumps(rest_api_data))

        resp_data = resp.json()

        return resp_data

    def update_gist(self, file_name, gist_id=None):

        file_name = Path(file_name)

        gist_ids = []
        if not gist_id:

            gist_list = self.get_gists()

            for k in gist_list:

                if file_name.name in k['files']:

                    gist_ids.append(k['id'])

            gist_id = gist_ids[0]

        if len(gist_ids) > 1:
            raise GISTAmbiguityError(gist_ids_list=gist_ids)

        _query_url = f'https://api.github.com/gists/{gist_id}'

        rest_api_data = self._readnparse_python_file(file_name)


        resp = requests.patch(_query_url, headers=self._headers, data=json.dumps(rest_api_data))

        resp_data = resp.json()

        return resp_data

    def delete_gist(self, gist_id):

        _query_url = f'https://api.github.com/gists/{gist_id}'

        resp = requests.delete(_query_url, headers=self._headers)

        resp_status = resp.status_code

        return resp_status
