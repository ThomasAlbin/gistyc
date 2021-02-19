import os
import time
import gistyc

def test_gistyc():
    
    auth_token = os.environ['gist_token']
    
    gist_api = gistyc.GISTyc(auth_token=auth_token)
    
   # response_data = gist_api.get_gists()
    
  #  print(response_data[0])
   # stop
    response_data = gist_api.create_gist(file_name=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                '_resources/create/sample.py'))

    print(response_data)
    stop
    response_data = gist_api.update_gist(file_name=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                '_resources/update/sample.py'))
    #print(response_data[0])
    #response_data = gist_api.delete_gist()
    