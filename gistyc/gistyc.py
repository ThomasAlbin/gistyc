import json
from pathlib import Path
import requests

class GISTAmbiguityError(Exception):

    def __init__(self, gist_ids_list, message="Number of GIST IDs is too ambiguous"):
        self.gist_ids_list = gist_ids_list
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}\nIDs: ' + ', '.join(self.gist_ids_list)

class GISTyc:
    
    def __init__(self, auth_token):
        
        self.auth_token = auth_token
        
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
            
            if index==0:            
                gist_code_dict[core_file_name] = {"content": k}
                
            else:
                gist_code_dict[core_file_name.replace('.py', f'_{index}.py')] = {"content": k}
            
        data = {"public" : True, "files" : gist_code_dict, }

        return data    

    def get_gists(self):
        
        _query_url = "https://api.github.com/gists?page=PAGE&per_page=100"
        
        _resp_ansr = True
        
        data = []
        
        cntr = 0
        while _resp_ansr:
            cntr += 1
            
            r = requests.get(_query_url.replace('PAGE', str(cntr)),
                             headers=self._headers)

            resp_content = r.json()
            
            if len(resp_content) > 0:
                data.extend(resp_content)
            else:
                _resp_ansr = False
    
        return data
    
    
    def create_gist(self, file_name):
        
        _query_url = "https://api.github.com/gists"
        
        rest_api_data = self._readnparse_python_file(file_name)
        

        r = requests.post(_query_url, headers=self._headers, data=json.dumps(rest_api_data))
           
        data = r.json()
        
        return data
        
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
            raise(GISTAmbiguityError(gist_ids_list=gist_ids))
        
        _query_url = f'https://api.github.com/gists/{gist_id}'
        
        rest_api_data = self._readnparse_python_file(file_name)
        

        r = requests.patch(_query_url, headers=self._headers, data=json.dumps(rest_api_data))
           
        data = r.json()
        
        return data
        
    def delete_gist(self, gist_id):
        
        _query_url = f'https://api.github.com/gists/{gist_id}'

        r = requests.delete(_query_url, headers=self._headers)
           
        data = r.status_code
        
        return data
        
        