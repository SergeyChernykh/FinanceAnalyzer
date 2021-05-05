import tkinter as tk


class StickyFrame(tk.Frame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback
        self.grid(sticky="NEWS")


class WindowAccounting(StickyFrame):
    def __init__(self, master, callback):
        super().__init__(master, callback)

    def __call__(self, data):
        pass


class WindowGoals(StickyFrame):
    def __init__(self, master, callback):
        super().__init__(master, callback)

    def __call__(self, data):
        pass


class WindowReport(StickyFrame):
    def __init__(self, master, callback):
        super().__init__(master, callback)

    def __call__(self, data):
        pass


class WindowSettings(StickyFrame):
    def __init__(self, master, callback):
        super().__init__(master, callback)

    def __call__(self, data):
        pass


class View:
    def __init__(self, master, callback):
        self.window_accounting = WindowAccounting(master, callback)
        self.window_goals = WindowGoals(master, callback)
        self.window_report = WindowReport(master, callback)
        self.window_setting = WindowSettings(master, callback)

    def __call__(self, window, data):
        getattr(self, window)(data)
