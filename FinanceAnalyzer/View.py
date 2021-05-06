import tkinter as tk
import re


class StickyFrame(tk.Frame):
    sep_geom = "", r"\.", r"\+", ":", r"\.", r"\+"
    re_geom = re.compile("".join((f"(?:{f}([0-9]*))?" for f in sep_geom)) + "(?:/([NEWSnews]+))?")

    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback
        self.grid(sticky="NEWS")
        self.main_frame, self.main_geom = self._(tk.Frame, self, "0:0.10")
        self.buttons_frame, self.buttons_geom = self._(tk.Frame, self, "0:1.1")
        self.accounting, self.accounting_geom = self._(tk.Button, self.buttons_frame, "0:0",
                                                       text="Accounting")
        self.goals, self.goals_geom = self._(tk.Button, self.buttons_frame, "1:0", text="Goals")
        self.report, self.report_geom = self._(tk.Button, self.buttons_frame, "2:0", text="Report")
        self.settings, self.settings_geom = self._(tk.Button, self.buttons_frame, "3:0",
                                                   text="Settings")
        self.active_objects = []

    def _(self, cls, master, geom=":", draw=False, *args, **kwargs):
        ret = cls(master, *args, **kwargs)
        groups = self.re_geom.match(geom or ":").groups()
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

    def __call__(self, *args):
        for obj in self.active_objects:
            obj.grid_remove()
        self.main_frame.grid(**self.main_geom)
        self.buttons_frame.grid(**self.buttons_geom)
        self.accounting.grid(**self.accounting_geom)
        self.goals.grid(**self.goals_geom)
        self.report.grid(**self.report_geom)
        self.settings.grid(**self.settings_geom)


class WindowAccounting(StickyFrame):
    def __init__(self, master, callback):
        super().__init__(master, callback)
        self.num_columns = 4
        self.canvas, self.canvas_geom = self._(tk.Canvas, self.main_frame, "0:0")
        self.scrollbar, self.scrollbar_geom = self._(tk.Scrollbar, self.main_frame, "0:1.0",
                                                     orient="vertical", command=self.canvas.yview)
        self.main_scrollable_frame, self.main_scrollable_geom = self._(tk.Frame, self.canvas,
                                                                       "0:0")
        self.main_scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.main_scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def __call__(self, data):
        super().__call__(data)
        self.canvas.grid(**self.canvas_geom)
        self.scrollbar.grid(**self.scrollbar_geom)
        self.active_objects += [self.canvas, self.scrollbar, self.main_scrollable_frame]
        self.active_objects.append(self._(tk.Label, self.main_scrollable_frame, "0:0", True,
                                          text="Comment"))
        self.active_objects.append(self._(tk.Label, self.main_scrollable_frame, "0:1", True,
                                          text="Category"))
        self.active_objects.append(self._(tk.Label, self.main_scrollable_frame, "0:2", True,
                                          text="Income/Expenses"))
        self.active_objects.append(self._(tk.Label, self.main_scrollable_frame, "0:3", True,
                                          text="Date"))
        for row, row_data in enumerate(data):
            for col in range(self.num_columns):
                self.active_objects.append(self._(tk.Text, self.main_scrollable_frame,
                                                  f"{row + 1}:{col}", True, width=20, height=1))
                self.active_objects[-1].insert(1.0, row_data[col])


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
