import json
from pathlib import Path
import requests
import os

class GISTyc:
    
    def __init__(self, auth_token):
        
        self.auth_token = auth_token
        
        self._headers = {'Authorization': f'token {auth_token}'}
        
        self.gists = []
        
    def get_gists(self):
        
        _query_url = "https://api.github.com/gists?page=PAGE&per_page=100"
        
        _resp_ansr = True
        
        cntr = 0
        while _resp_ansr:
            cntr += 1
            
            r = requests.get(_query_url.replace('PAGE', str(cntr)),
                             headers=self._headers)

            resp_content = r.json()
            
            if len(resp_content) > 0:
                self.gists.extend(resp_content)
            else:
                _resp_ansr = False
    
    def create_gist(self, file_name):
        
        _query_url = "https://api.github.com/gists"
        
        file_name = Path(file_name)
        
        with open(file_name, 'r') as file_obj:
            file_content = file_obj.read()
        
        core_file_name = file_name.name
        
        file_content = file_content.split('#%%')
        
        gist_code_dict = {}
        for index, k in enumerate(file_content):
            gist_code_dict[core_file_name.replace('.py', f'{index}.py')] = {"content": k}
            
        data = {"public" : True, "files" : gist_code_dict, }
        
        print(data)
      #  stop
        r = requests.post(_query_url, headers=self._headers, data=json.dumps(data))
            
        print(r.json())
        