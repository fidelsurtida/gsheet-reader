# ---------------------------------------------------
# settingsmanager.py - SettingsManager Class
# ---------------------------------------------------
# A custom flet control that encapsulates the UI for
# a settings window of this GSheet Reader App.
# It loads the saved settings from a json file in
# config folder. This will show the list of column
# names to fetch, starting row to read and other
# page settings to fetch data from.
# ---------------------------------------------------

import flet as ft


class SettingsManager(ft.Row):

    def __init__(self):
        """
        Custom Flet Control for showing the settings
        window. It manages the saving of settings into
        a json config file. All configurations will be
        used by the reader to determine the specific
        data to fetch.
        """

        super().__init__()

        self.controls = [
            ft.ElevatedButton("Dashboard",
                              on_click=lambda e: e.page.go("/dashboard")),
        ]
