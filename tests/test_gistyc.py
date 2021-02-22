import os
import time
import gistyc
import pytest

def test_gistyc_create_n_delete():
    
    auth_token = os.environ['gist_token']
    
    gist_api = gistyc.GISTyc(auth_token=auth_token)
    
   # response_data = gist_api.get_gists()
    
  #  print(response_data[0])
   # stop
    response_data = gist_api.create_gist(file_name=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                '_resources/create/sample.py'))

    assert 'sample.py' in response_data['files'].keys()

    # response_data = gist_api.update_gist(file_name=os.path.join(os.path.dirname(os.path.abspath(__file__)),
    #                                                             '_resources/update/sample.py'))
    #print(response_data[0])
    response_data = gist_api.delete_gist(response_data['id'])
    
    assert response_data == 204
    
def test_gistyc_create_n_update():
    
    auth_token = os.environ['gist_token']
    
    gist_api = gistyc.GISTyc(auth_token=auth_token)

    _ = gist_api.create_gist(file_name=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                '_resources/create/sample.py'))

    response_update_data = gist_api.update_gist(file_name=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                '_resources/update/sample.py'))

    assert response_update_data['updated_at'] > response_update_data['created_at']
    response_data = gist_api.delete_gist(response_update_data['id'])
    
    assert response_data == 204

def test_gistyc_create_n_update_id():
    
    auth_token = os.environ['gist_token']
    
    gist_api = gistyc.GISTyc(auth_token=auth_token)

    response_create_data = gist_api.create_gist(file_name=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                '_resources/create/sample.py'))

    response_update_data = gist_api.update_gist(file_name=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                '_resources/update/sample.py'), gist_id=response_create_data['id'])

    assert response_update_data['updated_at'] > response_update_data['created_at']
    response_data = gist_api.delete_gist(response_update_data['id'])
    
    assert response_data == 204
 

@pytest.mark.xfail(raises=gistyc.GISTAmbiguityError)
def test_gistyc_ambiguous():
    
    auth_token = os.environ['gist_token']
    
    gist_api = gistyc.GISTyc(auth_token=auth_token)

    response_create_1 = gist_api.create_gist(file_name=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                '_resources/create/sample.py'))

    response_create_2 = gist_api.create_gist(file_name=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                '_resources/create/sample.py'))
    
    _ = gist_api.update_gist(file_name=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                            '_resources/update/sample.py'))
def test_gistyc_clean_ambiguous():
    
    auth_token = os.environ['gist_token']
    
    gist_api = gistyc.GISTyc(auth_token=auth_token)
    
    response_gists_list = gist_api.get_gists()
    
    for k in response_gists_list:
        if 'sample.py' in k['files']:    
            response_data = gist_api.delete_gist(gist_id=k['id'])            
            assert response_data == 204

