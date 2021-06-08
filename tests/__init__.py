"""Test module."""
import tempfile
import unittest
import FinanceAnalyzer.Controller
import FinanceAnalyzer.Model


class TestFinanceAnalyzer(unittest.TestCase):
    """Test class."""

    def setUp(self):
        """Create controller and pass it empty db before each test."""
        self.dbfile = tempfile.NamedTemporaryFile()
        self.controller = FinanceAnalyzer.Controller.Controller(title="FinanceAnalyzer",
                                                                dbpath=self.dbfile.name)
        self.controller.model.create_tables()

    def test_0_create_tables(self):
        """Check initial content of tables."""
        res = self.controller.model.cur.execute("SELECT * FROM ACCOUNTING ORDER BY id")
        self.assertEqual(list(res), [(i, "", "", 0.0, "")
                                     for i in range(self.controller.model.num_records_start)])
        res = self.controller.model.cur.execute("SELECT * FROM SETTINGS ORDER BY name")
        res = list(res)
        self.assertEqual(len(res), 3)
        self.assertEqual(dict(res),
                         {"Background color": "white", "Text color": "black", "Font": "Arial"})

    def test_1_prepare_theme_data(self):
        """Check theme settings, prepared for Tkinter."""
        res = self.controller.model.prepare_theme_data()
        self.assertEqual(res, {"background": "white", "fg": "black", "font": "Arial"})

    def test_2_init(self):
        """Check initial theme settings in View."""
        self.assertEqual(self.controller.main_window.master.title(), "FinanceAnalyzer")
        self.controller.pass_event_to_model({"type": "start_setup", "data": None})
        self.assertEqual(self.controller.view.theme_info,
                         {"background": "white", "fg": "black", "font": "Arial"})

    def test_3_entry_edit(self):
        """Check that editing entry in accounting table really edits it in database."""
        self.controller.pass_event_to_model({"type": "start_setup", "data": None})
        entry0 = self.controller.view.window_accounting.entries[0, 0]
        entry0.focus_force()
        newtext = "bla-bla-bla"
        entry0.insert(0, newtext)
        root = self.controller.main_window.master

        def func():
            import time
            entry0.event_generate("<Return>")
            time.sleep(1)
            root.destroy()

        root.after(1000, func)
        root.mainloop()
        res = self.controller.model.cur.execute("SELECT * FROM ACCOUNTING ORDER BY id LIMIT 1")
        res = list(res)[0][1]
        self.assertEqual(res, newtext)

    def test_4_setting_theme(self):
        """Check that editing color settings really edits it in View and in database."""
        self.controller.pass_event_to_model({"type": "start_setup", "data": None})
        self.controller.pass_event_to_model({"type": "settings_navigation", "data": None})
        entry_name = self.controller.view.window_settings.entries[0, 0]
        entry_val = self.controller.view.window_settings.entries[0, 1]
        self.assertEqual(entry_name.cget("text"), "Background color")
        entry_val.focus_force()
        newcolor = "gray"
        entry_val.delete(0, "end")
        entry_val.insert(0, newcolor)
        root = self.controller.main_window.master

        def func():
            import time
            entry_val.event_generate("<Return>")
            time.sleep(1)
            self.assertEqual(self.controller.view.window_settings['bg'], newcolor)
            root.destroy()

        root.after(1000, func)
        root.mainloop()
        res = self.controller.model.cur.execute("SELECT value FROM SETTINGS"
                                                " WHERE name='Background color'")
        res = list(res)[0][0]
        self.assertEqual(res, newcolor)

    def cleanUp(self):
        """Close temporary file after each test."""
        self.dbfile.close()
