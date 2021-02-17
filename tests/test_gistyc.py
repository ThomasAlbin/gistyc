import os

import gistyc

def test_gistyc():
    
    auth_token = os.environ['gist_token']
    
    gist_api = gistyc.GISTyc(auth_token=auth_token)
    
    #gist_api.get_gists()
    
    #print(len(gist_api.gists))
    
    gist_api.create_gist(file_name=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                '_resources/create/sample.py'))

    gist_api.update_gist(file_name=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                '_resources/update/sample.py'))
    
    pass