import tkinter as tk
from . import View, Model


class Controller:
    def __init__(self, title="FinanceAnalyzer"):
        self.main_window = tk.Frame()
        self.main_window.master.geometry("1280x720")
        self.main_window.master.title(title)
        self.main_window.master.columnconfigure(0, weight=1)
        self.main_window.master.rowconfigure(0, weight=1)
        self.main_window.columnconfigure(0, weight=1)
        self.main_window.rowconfigure(0, weight=1)
        self.main_window.grid(sticky="NEWS")
        self.view = View.View(self.main_window, self.pass_event_to_model)
        self.model = Model.Model(self.draw_view)

    def __call__(self):
        self.pass_event_to_model()
        self.main_window.master.mainloop()

    def pass_event_to_model(self, window=None, event=None):
        self.model(window, event)

    def draw_view(self, window, data):
        self.view(window, data)


def main():
    controller = Controller(title="FinanceAnalyzer")
    controller()
