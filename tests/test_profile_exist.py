import pytest

from msa_sdk.profile import Profile


class DummyResponse:
    def __init__(self, status_code):
        self.status_code = status_code

class DummyProfile(Profile):
    def _call_get(self):
        # This will be set in the test
        pass

def test_exist_returns_true(monkeypatch):
    profile = DummyProfile()
    def fake_call_get():
        profile.response = DummyResponse(200)
    profile._call_get = fake_call_get
    assert profile.exist('ref1') is True

def test_exist_returns_false(monkeypatch):
    profile = DummyProfile()
    def fake_call_get():
        profile.response = DummyResponse(404)
    profile._call_get = fake_call_get
    assert profile.exist('ref2') is False


def test_exist_raises_no_response(monkeypatch):
    profile = DummyProfile()
    def fake_call_get():
        profile.response = None
    profile._call_get = fake_call_get
    with pytest.raises(Exception, match="No response received from the server."):
        profile.exist('ref3')


def test_exist_raises_unexpected_code(monkeypatch):
    profile = DummyProfile()
    def fake_call_get():
        profile.response = DummyResponse(500)
    profile._call_get = fake_call_get
    with pytest.raises(Exception, match="Unexpected response code: 500"):
        profile.exist('ref4')
