class Model:
    def __init__(self, callback):
        self.callback = callback

    def __call__(self, window, event):
        window = window if window is not None else "window_accounting"
        event = event if event is not None else "show"
        assert self.validate_args(window, event)
        window, data = self.process_event(window, event)
        self.callback(window, data)

    @staticmethod
    def validate_args(window, event):
        return True

    @staticmethod
    def process_event(window, event):
        return window, None
