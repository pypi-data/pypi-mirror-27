import json

import falcon


class LED:

    def __init__(self, leds):
        self._leds = leds

    def _led_to_dict(self, led):
        return {
            'pin': led.pin,
            'is_lit': led.is_lit
        }

    def _led_to_json(self, led):
        return json.dumps(self._led_to_dict(led))


class Detail(LED):

    def on_get(self, req, res, label):
        led = self._leds.get(label)
        if led is None:
            raise falcon.HTTPNotFound()
        res.body = self._led_to_json(led)


class List(LED):

    def on_get(self, req, res):
        result = []
        for label in self._leds:
            result.append({
                'route': '/{0}'.format(label)
            })
        res.body = json.dumps(result)


class Control(LED):

    allowed_actions = ('on', 'off', 'toggle')

    def on_post(self, req, res, label, action):
        led = self._leds.get(label)
        if led is None or action not in self.allowed_actions:
            raise falcon.HTTPNotFound()

        getattr(led, action)()
        res.body = self._led_to_json(led)
