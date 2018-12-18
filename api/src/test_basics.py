from flask import url_for


def test_app_connection(app):
    assert app.name == 'src'


def test_ping(client):
    resp = client.get(url_for('etc.ping'))
    assert resp.status_code == 200
    assert resp.json['ping'] == 'pong'