import tkinter as tk
import re


class WindowAccounting(tk.Frame):
    def __init__(self, master, callback):
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
        self.comment = View.fc(tk.Label, self.main_scrollable_frame, "0:0", True, text="Comment")
        self.category = View.fc(tk.Label, self.main_scrollable_frame, "0:1", True, text="Category")
        self.value = View.fc(tk.Label, self.main_scrollable_frame, "0:2", True,
                             text="Income/Expenses")
        self.data = View.fc(tk.Label, self.main_scrollable_frame, "0:3", True, text="Date")
        self.entries = {}

    def __call__(self, data):
        for entry in data:
            row, col = entry["row"], entry["col"]
            self.entries[row, col] = View.fc(tk.Entry, self.main_scrollable_frame,
                                             f"{row + 1}:{col}", True)
            self.entries[row, col].insert(0, entry["data"])


class WindowGoals(tk.Frame):
    def __init__(self, master, callback):
        super().__init__(master)

    def __call__(self, data):
        pass


class WindowReport(tk.Frame):
    def __init__(self, master, callback):
        super().__init__(master)

    def __call__(self, data):
        pass


class WindowSettings(tk.Frame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback
        self.entries = {}

    def __call__(self, data):
        for entry in data:
            row, col, data = entry["row"], entry["col"], entry["data"]
            if col == 0:
                self.entries[row, col] = View.fc(tk.Label, self, f"{row + 1}.0:{col}", True,
                                                 text=data)
            else:
                self.entries[row, col] = View.fc(tk.Entry, self, f"{row + 1}.0:{col}", True)
                self.entries[row, col].insert(0, data)


class View:
    sep_geom = "", r"\.", r"\+", ":", r"\.", r"\+"
    re_geom = re.compile("".join((f"(?:{f}([0-9]*))?" for f in sep_geom)) + "(?:/([NEWSnews]+))?")
    active_objects = []

    def __init__(self, master, callback):
        self.callback = callback
        self.main_frame = self.fc(tk.Frame, master, "0:0.10", True)
        self.buttons_frame = self.fc(tk.Frame, master, "0:1.1", True)
        self.accounting = self.fc(tk.Button, self.buttons_frame, "0:0", True, text="Accounting",
                                  command=lambda: self.callback({"type": "accounting_navigation",
                                                                 "data": None}))
        self.goals = self.fc(tk.Button, self.buttons_frame, "1:0", True, text="Goals")
        self.report = self.fc(tk.Button, self.buttons_frame, "2:0", True, text="Report")
        self.settings = self.fc(tk.Button, self.buttons_frame, "3:0", True, text="Settings",
                                command=lambda: self.callback({"type": "settings_navigation",
                                                               "data": None}))
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.window_accounting = WindowAccounting(self.main_frame, callback)
        self.window_goals = WindowGoals(self.main_frame, callback)
        self.window_report = WindowReport(self.main_frame, callback)
        self.window_settings = WindowSettings(self.main_frame, callback)

    def __call__(self, window, data):
        self.window_accounting.grid_remove()
        self.window_goals.grid_remove()
        self.window_report.grid_remove()
        self.window_settings.grid_remove()
        getattr(self, window).grid(sticky="NEWS")
        getattr(self, window)(data)

    @staticmethod
    def fc(cls, master, geom=":", draw=False, *args, **kwargs):
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
