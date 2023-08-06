import falcon

from .resources import Control, Detail, List


def create(pin_config, led_factory):
    """
    This returns a Falcon application that is ready to use with Gunicorn.
    `pin_config`: An iterable of pin number/route label pairs
    `led_factory`: A factory creating LED class instances
    """

    leds = {label: led_factory(pin) for label, pin in pin_config}

    app = falcon.API()
    app.add_route('/', List(leds=leds))
    app.add_route('/{label}', Detail(leds=leds))
    app.add_route('/{label}/{action}', Control(leds=leds))

    return app
