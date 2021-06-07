"""MVC Controller part of application."""
import tkinter as tk
from . import View, Model
from typing import Optional, Dict, Union, Iterable


class Controller:
    """MVC Controller class."""

    def __init__(self, title: str = "FinanceAnalyzer") -> None:
        """Create View and Model instances.

        Model and View communicate via callbacks.
        :param title: application title.
        """
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
        self.window = "window_main"

    def __call__(self) -> None:
        """Initialize communications between Model and View."""
        self.pass_event_to_model(self.main_window, {"type": "start_setup", "data": None})
        self.main_window.master.mainloop()

    def pass_event_to_model(self, event: Dict[str, Optional[Union[str, int]]] = None) -> None:
        """Pass data to Model."""
        self.model(self.window, event)

    def draw_view(self, window: str,
                  data: Optional[Union[Iterable[Dict[str, Union[int, str, float]]],
                                       Dict[str, str]]]) -> None:
        """Pass data to View."""
        self.window = window
        self.view(window, data)


def main():
    """Start application."""
    controller = Controller(title="FinanceAnalyzer")
    controller()
