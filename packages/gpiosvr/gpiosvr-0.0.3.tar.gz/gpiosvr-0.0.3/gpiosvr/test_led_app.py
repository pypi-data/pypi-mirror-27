from unittest import mock

from falcon import testing
import pytest

from .led import app


PIN_CONFIG = [('red', 5), ('blue', 13)]
VALID_ACTIONS = ('on', 'off', 'toggle', )
INVALID_ACTIONS = ('this', 'that', 'whatever', )


def action_routes(actions):
    for label, _ in PIN_CONFIG:
        for action in actions:
            yield '/{0}/{1}'.format(label, action)


def mock_led_factory(pin_num):
    m = mock.MagicMock()
    m.is_lit = False
    m.pin = pin_num
    return m


@pytest.fixture()
def client():
    a = app.create(pin_config=PIN_CONFIG, led_factory=mock_led_factory)
    return testing.TestClient(a)


def test_get_led_routes_list(client):
    result = client.simulate_get('/')
    assert result.status_code == 200
    assert len(result.json) == len(PIN_CONFIG)


def test_get_led_exists(client):
    for label, pin in PIN_CONFIG:
        result = client.simulate_get('/{0}'.format(label))
        assert result.json['pin'] == pin
        assert result.json['is_lit'] is False


def test_get_led_not_exists(client):
    result = client.simulate_get('/green')
    assert result.status_code == 404


def test_valid_led_actions(client):
    for route in action_routes(VALID_ACTIONS):
        result = client.simulate_post(route)
        assert result.status_code == 200
        assert result.json.get('pin') is not None
        assert result.json.get('is_lit') is not None


def test_invalid_led_actions(client):
    for route in action_routes(INVALID_ACTIONS):
        result = client.simulate_post(route)
        assert result.status_code == 404
