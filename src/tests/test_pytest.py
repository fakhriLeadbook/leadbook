import json

def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200
    expected = "Leadbook Test 2"
    assert expected == res.get_data(as_text=True)


