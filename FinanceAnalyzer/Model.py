import os
import sqlite3


class Model:
    def __init__(self, callback):
        self.callback = callback
        self.windows = {"window_accounting", "window_settings"}
        self.settings_set = {"Background color", "Text color", "Font"}
        self.initial_call = {w: True for w in self.windows}
        self.con = sqlite3.connect(os.path.expanduser("~/FinanceAnalyzer.db"))
        self.cur = self.con.cursor()
        self.num_records_start = 20

    def __del__(self):
        self.con.commit()
        self.con.close()

    def __call__(self, window, event):
        window = window if window is not None else "window_main"
        event = event if event is not None else {"type": "start_setup", "data": None}
        assert self.validate_args(window, event)
        window, data = self.process_event(event)
        self.callback(window, data)

    @staticmethod
    def validate_args(window, event):
        return True

    def start_setup(self, event):
        window = "window_main"
        try:
            self.cur.execute("SELECT * FROM ACCOUNTING LIMIT 1")
            self.cur.execute("SELECT * FROM SETTINGS LIMIT 1")
        except sqlite3.OperationalError:
            self.create_tables()
        return window, self.prepare_theme_data()

    def prepare_theme_data(self):
        res = self.cur.execute("SELECT * FROM SETTINGS ORDER BY name")
        tmpres = {record[0]: record[1] for record in res if record[0] in self.settings_set}
        fullname2tk = {"Background color": "background", "Text color": "fg", "Font": "font"}
        return {fullname2tk[k]: v for k, v in tmpres.items()}

    def create_tables(self):
        self.cur.execute("CREATE TABLE ACCOUNTING"
                         "(id integer,"
                         "comment text,"
                         "category text,"
                         "value real,"
                         "date text)")
        self.cur.executemany("INSERT INTO ACCOUNTING VALUES (?, ?, ?, ?, ?)",
                             [(i, "", "", 0.0, "") for i in range(self.num_records_start)])
        self.cur.execute("CREATE TABLE SETTINGS"
                         "(name text,"
                         "value text)")
        self.cur.executemany("INSERT INTO SETTINGS VALUES (?, ?)",
                             [("Background color", "white"), ("Text color", "black"),
                              ("Font", "Arial")])

    def accounting_navigation(self, event):
        window = "window_accounting"
        if self.initial_call[window]:
            self.initial_call[window] = False
            res = self.cur.execute("SELECT * FROM ACCOUNTING ORDER BY id")
            result = []
            for row, record in enumerate(res):
                for col, val in enumerate(record):
                    if col != 0:
                        result.append({"row": row, "col": col - 1, "data": val if val else ""})
            return window, result
        else:
            return window, []

    def accounting_update_row(self, event):
        window = "window_accounting"
        self.cur.execute("UPDATE ACCOUNTING SET comment=:comment, category=:category, "
                         "value=:value, date=:date WHERE id=:id", event)
        if event["id"] % 20 == 19:
            self.cur.executemany("INSERT INTO ACCOUNTING VALUES (?, ?, ?, ?, ?)",
                                 [(event["id"] + 1 + i, "", "", 0.0, "")
                                  for i in range(self.num_records_start)])
            res = self.cur.execute("SELECT * FROM ACCOUNTING ORDER BY id")
            result = [{"row": row, "col": col - 1, "data": val if val else ""}
                      for row, record in enumerate(res)
                      for col, val in enumerate(record) if col != 0]
            return window, result
        return window, []

    def settings_navigation(self, event):
        window = "window_settings"
        if self.initial_call[window]:
            self.initial_call[window] = False
            res = self.cur.execute("SELECT * FROM SETTINGS ORDER BY name ")
            result = [{"row": row, "col": col, "data": val}
                      for row, record in enumerate(res)
                      for col, val in enumerate(record)]
            return window, result
        return window, []

    def process_event(self, event):
        return getattr(self, event["type"])(event)

    def theme_setup(self, event):
        window = "window_settings"
        if self.initial_call[window]:
            return self.accounting_navigation(event)
        else:
            return self.settings_navigation(event)

    def settings_update_row(self, event):
        window = "window_main"
        self.cur.execute("UPDATE SETTINGS SET value=:value WHERE name=:name", event)
        return window, self.prepare_theme_data()
