import json

def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200
    expected = "Leadbook Test"
    assert expected == res.get_data(as_text=True)


def test_upload(app, client):


    headers = {
        'Content-Type': 'application/json'
    }

    
    data = {"bucket": "senz-testing", "file": "Leadbook/data-2018.txt"}
    url = '/insert'

    res = client.post(url, data=json.dumps(data), headers=headers)

    assert res.status_code == 200
    expected = {'result' : "success"}
    assert expected == json.loads(res.get_data(as_text=True))


    
    # # Yang asli
    # mimetype = 'application/json'
    # headers = {
    #     'Content-Type': mimetype,
    #     'Accept': mimetype
    # }

    
    # data = {"bucket": "senz-testing", "file": "Leadbook/data-2018.txt"}
    # url = '/insert'

    # res = client.post(url, data=json.dumps(data), headers=headers)

    # assert res.content_type == mimetype
    # assert res.status_code == 200
    # expected = {'result' : "success"}
    # assert expected == json.loads(res.get_data(as_text=True))


    
