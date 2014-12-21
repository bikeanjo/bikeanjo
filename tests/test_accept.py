from .. import bikeanjo

def test_home(rf):
    request = rf.get('/')
    assert bikeanjo.home(request)


def test_with_client(client, db):
    response = client.get('/')
    assert '<!DOCTYPE html>' in response.content
