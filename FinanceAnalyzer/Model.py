"""MVC Model part of application."""
import os
import sqlite3
from typing import Optional, Dict, Union, Callable, Iterable, Tuple


class Model:
    """MVC Model class."""

    def __init__(self, callback: Callable[[str, Optional[
            Union[Iterable[Dict[str, Union[int, str, float]]], Dict[str, str]]]], None]) -> None:
        """Open database.

        :param callback: callback passed by Controller.
        """
        self.callback = callback
        self.windows = {"window_accounting", "window_settings"}
        self.settings_set = {"Background color", "Text color", "Font"}
        self.initial_call = {w: True for w in self.windows}
        self.con = sqlite3.connect(os.path.expanduser("~/FinanceAnalyzer.db"))
        self.cur = self.con.cursor()
        self.num_records_start = 20

    def __del__(self) -> None:
        """Commit changes and close database."""
        self.con.commit()
        self.con.close()

    def __call__(self, window: str, event: Dict[str, Optional[Union[str, int]]]) -> None:
        """Process event and pass data to Controller.

        :param window: the window in which the event occurred.
        :param event: occurred event data.
        """
        assert self.validate_args(window, event)
        window, data = self.process_event(event)
        self.callback(window, data)

    @staticmethod
    def validate_args(window: str, event: Dict[str, Optional[Union[str, int]]]) -> bool:
        """Validate data passed from Controller.

        :param window: the window in which the event occurred.
        :param event: occurred event data.
        """
        return True

    def start_setup(self, event: Dict[str, Optional[Union[str, int]]]
                    ) -> Tuple[str, Dict[str, str]]:
        """Check if database empty. Crete tables if needed.

        :param event: occurred event data.
        """
        window = "window_main"
        try:
            self.cur.execute("SELECT * FROM ACCOUNTING LIMIT 1")
            self.cur.execute("SELECT * FROM SETTINGS LIMIT 1")
        except sqlite3.OperationalError:
            self.create_tables()
        return window, self.prepare_theme_data()

    def prepare_theme_data(self) -> Dict[str, str]:
        """Get theme settings from database."""
        res = self.cur.execute("SELECT * FROM SETTINGS ORDER BY name")
        tmpres = {record[0]: record[1] for record in res if record[0] in self.settings_set}
        fullname2tk = {"Background color": "background", "Text color": "fg", "Font": "font"}
        return {fullname2tk[k]: v for k, v in tmpres.items()}

    def create_tables(self) -> None:
        """Create Accounting and Settings tables."""
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

    def accounting_navigation(self, event: Dict[str, Optional[Union[str, int]]]
                              ) -> Tuple[str, Iterable[Dict[str, Union[int, float, str]]]]:
        """Prepare data to draw Accounting window.

        Return data only on first call, because View store them too.
        :param event: occurred event data.
        """
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

    def accounting_update_row(self, event: Dict[str, Optional[Union[str, int]]]
                              ) -> Tuple[str, Iterable[Dict[str, Union[int, float, str]]]]:
        """Update changed entry in database.

        If last row was modified, add new entries.
        :param event: occurred event data.
        """
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

    def settings_navigation(self, event: Dict[str, Optional[Union[str, int]]]
                            ) -> Tuple[str, Iterable[Dict[str, Union[int, float, str]]]]:
        """Prepare data to draw Settings window.

        Return data only on first call, because View store them too.
        :param event: occurred event data.
        """
        window = "window_settings"
        if self.initial_call[window]:
            self.initial_call[window] = False
            res = self.cur.execute("SELECT * FROM SETTINGS ORDER BY name ")
            result = [{"row": row, "col": col, "data": val}
                      for row, record in enumerate(res)
                      for col, val in enumerate(record)]
            return window, result
        return window, []

    def process_event(self, event: Dict[str, Optional[Union[str, int]]]
                      ) -> Tuple[str, Union[Iterable[Dict[str, Union[int, float, str]]],
                                            Dict[str, str]]]:
        """Call event corresponding handler function.

        :param event: occurred event data.
        """
        return getattr(self, event["type"])(event)

    def theme_setup(self, event: Dict[str, Optional[Union[str, int]]]) -> Tuple[str, Iterable]:
        """Navigate after theme was applied.

        :param event: occurred event data.
        """
        window = "window_settings"
        if self.initial_call[window]:
            return self.accounting_navigation(event)
        else:
            return self.settings_navigation(event)

    def settings_update_row(self, event: Dict[str, Optional[Union[str, int]]]
                            ) -> Tuple[str, Iterable]:
        """Update changed setting in database.

        :param event: occurred event data.
        """
        window = "window_main"
        self.cur.execute("UPDATE SETTINGS SET value=:value WHERE name=:name", event)
        return window, self.prepare_theme_data()
