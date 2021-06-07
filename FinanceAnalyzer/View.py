"""MVC View part of application."""
import os
import re
import gettext
import tkinter as tk
from typing import Optional, Dict, Union, Callable, Iterable, Tuple


gettext.install("FinanceAnalyzer", os.path.dirname(__file__), names=("ngettext", ))


class WindowAccounting(tk.Frame):
    """WindowAccounting frame."""

    def __init__(self, master: Optional[tk.Frame],
                 callback: Callable[[Dict[str, Optional[Union[str, int]]]], None]
                 ) -> None:
        """Create nested frames.

        :param master: master frame.
        :param callback: callback passed by Controller.
        """
        super().__init__(master)
        self.num_columns = 4
        self.callback = callback
        self.canvas = View.fc(tk.Canvas, self, "0:0", True)
        self.scrollbar = View.fc(tk.Scrollbar, self, "0:1.0", True, orient="vertical",
                                 command=self.canvas.yview)
        self.main_scrollable_frame, unused = View.fc(tk.Frame, self.canvas, "0:0")
        self.main_scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.main_scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.comment = View.fc(tk.Label, self.main_scrollable_frame, "0:0", True,
                               text=_("Comment"))
        self.category = View.fc(tk.Label, self.main_scrollable_frame, "0:1", True,
                                text=_("Category"))
        self.value = View.fc(tk.Label, self.main_scrollable_frame, "0:2", True,
                             text=_("Income/Expenses"))
        self.data = View.fc(tk.Label, self.main_scrollable_frame, "0:3", True, text=_("Date"))
        self.entries = {}

    def __call__(self, data: Iterable[Dict[str, Union[int, str, float]]],
                 theme_info: Dict[str, str]) -> None:
        """Draw passed entries.

        :param data: entries data.
        :param theme_info: theme settings.
        """
        for entry in data:
            row, col = entry["row"], entry["col"]
            self.entries[row, col] = View.fc(tk.Entry, self.main_scrollable_frame,
                                             f"{row + 1}:{col}", True, **theme_info)
            self.entries[row, col].insert(0, entry["data"])
            self.entries[row, col].bind('<Return>', lambda _, row=row: self.update_row(row))

    def update_row(self, row: int) -> None:
        """Pass edited data to Controller.

        :param row: row number.
        """
        self.callback({"type": "accounting_update_row",
                       "id": row,
                       "comment": self.entries[row, 0].get(),
                       "category": self.entries[row, 1].get(),
                       "value": self.entries[row, 2].get(),
                       "date": self.entries[row, 3].get()
                       })


class WindowGoals(tk.Frame):
    """WindowGoals frame."""

    def __init__(self, master: Optional[tk.Frame],
                 callback: Callable[[Dict[str, Optional[Union[str, int]]]], None]
                 ) -> None:
        """Create nested frames.

        :param master: master frame.
        :param callback: callback passed by Controller.
        """
        super().__init__(master)

    def __call__(self, data: Iterable[Dict[str, Union[int, str, float]]],
                 theme_info: Dict[str, str]) -> None:
        """Draw passed data.

        :param data: entries data.
        :param theme_info: theme settings.
        """
        pass


class WindowReport(tk.Frame):
    """WindowReport frame."""

    def __init__(self, master: Optional[tk.Frame],
                 callback: Callable[[Dict[str, Optional[Union[str, int]]]], None]
                 ) -> None:
        """Create nested frames.

        :param master: master frame.
        :param callback: callback passed by Controller.
        """
        super().__init__(master)

    def __call__(self, data: Iterable[Dict[str, Union[int, str, float]]],
                 theme_info: Dict[str, str]) -> None:
        """Draw passed data.

        :param data: entries data.
        :param theme_info: theme settings.
        """
        pass


class WindowSettings(tk.Frame):
    """WindowSettings frame."""

    def __init__(self, master: Optional[tk.Frame],
                 callback: Callable[[Dict[str, Optional[Union[str, int]]]], None]
                 ) -> None:
        """Create nested frames.

        :param master: master frame.
        :param callback: callback passed by Controller.
        """
        super().__init__(master)
        self.callback = callback
        self.entries = {}

    def __call__(self, data: Iterable[Dict[str, Union[int, str, float]]],
                 theme_info: Dict[str, str]) -> None:
        """Draw passed entries.

        :param data: entries data.
        :param theme_info: theme settings.
        """
        for entry in data:
            row, col, entry_data = entry["row"], entry["col"], entry["data"]
            if col == 0:
                self.entries[row, col] = View.fc(tk.Label, self, f"{row + 1}.0:{col}", True,
                                                 text=entry_data, **theme_info)
            else:
                self.entries[row, col] = View.fc(tk.Entry, self, f"{row + 1}.0:{col}", True,
                                                 **theme_info)
                self.entries[row, col].insert(0, entry_data)
                self.entries[row, col].bind('<Return>', lambda _, row=row: self.update_row(row))

    def update_row(self, row: int) -> None:
        """Pass edited data to Controller.

        :param row: row number.
        """
        self.callback({"type": "settings_update_row",
                       "name": self.entries[row, 0].cget("text"),
                       "value": self.entries[row, 1].get(),
                       })


class View:
    """MVC View class."""

    sep_geom = "", r"\.", r"\+", ":", r"\.", r"\+"
    re_geom = re.compile("".join((f"(?:{f}([0-9]*))?" for f in sep_geom)) + "(?:/([NEWSnews]+))?")

    def __init__(self, master: Optional[tk.Frame],
                 callback: Callable[[Dict[str, Optional[Union[str, int]]]], None]
                 ) -> None:
        """Create nested frames.

        :param master: master frame.
        :param callback: callback passed by Controller.
        """
        self.callback = callback
        self.main_frame = self.fc(tk.Frame, master, "0:0.10", True)
        self.buttons_frame = self.fc(tk.Frame, master, "0:1.1", True)
        self.accounting = self.fc(tk.Button, self.buttons_frame, "0:0", True, text=_("Accounting"),
                                  command=lambda: self.callback({"type": "accounting_navigation",
                                                                 "data": None}))
        self.goals = self.fc(tk.Button, self.buttons_frame, "1:0", True, text=_("Goals"))
        self.report = self.fc(tk.Button, self.buttons_frame, "2:0", True, text=_("Report"))
        self.settings = self.fc(tk.Button, self.buttons_frame, "3:0", True, text=_("Settings"),
                                command=lambda: self.callback({"type": "settings_navigation",
                                                               "data": None}))
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.window_accounting = WindowAccounting(self.main_frame, callback)
        self.window_goals = WindowGoals(self.main_frame, callback)
        self.window_report = WindowReport(self.main_frame, callback)
        self.window_settings = WindowSettings(self.main_frame, callback)

    def setup_theme(self, theme_info: Dict[str, str]) -> None:
        """Change theme in all nested frames and store settings.

        :param theme_info: theme settings.
        """
        self.theme_info = theme_info
        self.window_accounting.configure(background=theme_info["background"])
        self.window_goals.configure(background=theme_info["background"])
        self.window_report.configure(background=theme_info["background"])
        self.window_settings.configure(background=theme_info["background"])

        self.accounting.configure(**theme_info)
        self.goals.configure(**theme_info)
        self.report.configure(**theme_info)
        self.settings.configure(**theme_info)

        self.window_accounting.comment.configure(**theme_info)
        self.window_accounting.category.configure(**theme_info)
        self.window_accounting.value.configure(**theme_info)
        self.window_accounting.data.configure(**theme_info)
        for entry in self.window_accounting.entries.values():
            entry.configure(**theme_info)

        for entry in self.window_settings.entries.values():
            entry.configure(**theme_info)

        self.callback({"type": "theme_setup", "data": None})

    def __call__(self, window: str,
                 data: Optional[Union[Iterable[Dict[str, Union[int, str, float]]],
                                      Dict[str, str]]]) -> None:
        """Pass data to draw in appropriate window.

        :param window: window to draw.
        :param data: data to draw.
        """
        self.window_accounting.grid_remove()
        self.window_goals.grid_remove()
        self.window_report.grid_remove()
        self.window_settings.grid_remove()
        if window == "window_main":
            self.setup_theme(data)
        else:
            getattr(self, window).grid(sticky="NEWS")
            getattr(self, window)(data, self.theme_info)

    @staticmethod
    def fc(cls: type, master: tk.Frame, geom: str = ":", draw: bool = False,
           *args,
           **kwargs) -> Union[tk.Frame, Tuple[tk.Frame, Dict[str, int]]]:
        """Create a widget, set up geometry and adjust master's column/row weights.
        Geometry string may (not) include any of the following fields:
        row+span.weight:row+column.weight/gravity

        :param cls: widget class
        :param master: master widget to embed
        :param geom: geometry string
        :param draw: need to draw
        :param args: positional arguments tuple for cls() call
        :param kwargs: named arguments tuple for cls() call
        """
        ret = cls(master, *args, **kwargs)
        groups = View.re_geom.match(geom or ":").groups()
        default = 0, 1, 0, master.grid_size()[0], 1, 0, "NEWS"
        y, wy, dy, x, wx, dx, s = (b if a in ('', None) else a for a, b in zip(groups, default))
        geom = {"column": x, "columnspan": int(dx) + 1, "row": y, "rowspan": int(dy) + 1,
                "sticky": s}
        master.rowconfigure(y, weight=wy)
        master.columnconfigure(x, weight=wx)
        if draw:
            ret.grid(**geom)
            return ret
        else:
            return ret, geom
