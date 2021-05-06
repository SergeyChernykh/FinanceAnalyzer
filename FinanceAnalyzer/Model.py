class Model:
    def __init__(self, callback):
        self.callback = callback
        self.windows = {"window_accounting", "window_settings"}
        self.initial_call = {w: True for w in self.windows}

    def __call__(self, window, event):
        window = window if window is not None else "window_accounting"
        event = event if event is not None else {"type": "accounting_navigation", "data": None}
        assert self.validate_args(window, event)
        window, data = self.process_event(window, event)
        self.callback(window, data)

    @staticmethod
    def validate_args(window, event):
        return True

    def process_event(self, window, event):
        event_type = event["type"]
        if event_type == "accounting_navigation":
            window = "window_accounting"
            if self.initial_call[window]:
                self.initial_call[window] = False
                return window, [{"row": i // 4, "col": i % 4, "data": f"{i}"} for i in range(80)]
            else:
                return window, []
        elif event_type == "settings_navigation":
            window = "window_settings"
            if self.initial_call[window]:
                return window, [{"row": i // 2, "col": i % 2, "data": f"{i}"} for i in range(40)]
            else:
                return window, []
