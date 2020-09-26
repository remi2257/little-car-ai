class Widget(object):
    def __init__(self, **kwargs):
        if "on_press" not in kwargs:
            self._on_press_cb = None
        else:
            self._on_press_cb = kwargs["on_press"]

    def on_press(self, **kwargs):
        if self._on_press_cb is None:
            pass
        else:
            self._on_press_cb(**kwargs)
