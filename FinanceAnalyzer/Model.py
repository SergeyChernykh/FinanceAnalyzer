import os
import sqlite3


class Model:
    def __init__(self, callback):
        self.callback = callback
        self.windows = {"window_accounting", "window_settings"}
        self.initial_call = {w: True for w in self.windows}
        self.con = sqlite3.connect(os.path.expanduser("~/FinanceAnalyzer.db"))
        self.cur = self.con.cursor()
        self.num_records_start = 20

    def __del__(self):
        self.con.commit()
        self.con.close()

    def __call__(self, window, event):
        window = window if window is not None else "window_accounting"
        event = event if event is not None else {"type": "accounting_navigation", "data": None}
        assert self.validate_args(window, event)
        window, data = self.process_event(window, event)
        self.callback(window, data)

    @staticmethod
    def validate_args(window, event):
        return True

    @property
    def accounting_navigation(self):
        window = "window_accounting"
        if self.initial_call[window]:
            self.initial_call[window] = False
            try:
                res = self.cur.execute("SELECT * FROM ACCOUNTING ORDER BY id")
                result = []
                for row, record in enumerate(res):
                    for col, val in enumerate(record):
                        if col != 0:
                            result.append({"row": row, "col": col - 1, "data": val if val else ""})
                return window, result
            except sqlite3.OperationalError:
                self.cur.execute("CREATE TABLE ACCOUNTING"
                                 "(id integer,"
                                 "comment text,"
                                 "category text,"
                                 "value real,"
                                 "date text)")
                self.cur.executemany("INSERT INTO ACCOUNTING VALUES (?, ?, ?, ?, ?)",
                                     [(i, "", "", 0.0, "")
                                      for i in range(self.num_records_start)])
                return window, ({"row": i // 4, "col": i % 4, "data": ""} for i in range(
                    self.num_records_start * 4))
        else:
            return window, []

    def accounting_row_update(self, event):
        upd = ""
        for column in ["comment", "category", "value", "date"]:
            upd += column + " = '" + event[column] + "',"
        self.cur.execute("update ACCOUNTING SET " + upd[:-1] + " WHERE id = " + str(event["id"]))
        if event["id"] % 20 == 19:
            self.cur.executemany("INSERT INTO ACCOUNTING VALUES (?, ?, ?, ?, ?)",
                                 [(event["id"] + 1 + i, "", "", 0.0, "")
                                  for i in range(self.num_records_start)])
            res = self.cur.execute("SELECT * FROM ACCOUNTING ORDER BY id")
            result = [{"row": row, "col": col - 1, "data": val if val else ""}
                      for row, record in enumerate(res)
                      for col, val in enumerate(record) if col != 0]
            return result
        return []

    def process_event(self, window, event):
        event_type = event["type"]
        if event_type == "accounting_navigation":
            return self.accounting_navigation
        elif event_type == "settings_navigation":
            window = "window_settings"
            if self.initial_call[window]:
                return window, [{"row": i // 2, "col": i % 2, "data": f"{i}"} for i in range(40)]
            else:
                return window, []
        elif event_type == "accounting_update_row":
            return window, self.accounting_row_update(event)
