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
import json
from modules.reader import Reader


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

        # File Path of the settings config
        self.settings_path = Reader.BASE_PATH / "config/settings.json"

        # Declaration of Flet control references
        self._date_col = ft.Ref[ft.TextField]()
        self._date_name = ft.Ref[ft.TextField]()
        self._start_time_col = ft.Ref[ft.TextField]()
        self._start_time_name = ft.Ref[ft.TextField]()
        self._end_time_col = ft.Ref[ft.TextField]()
        self._end_time_name = ft.Ref[ft.TextField]()

        self.controls = [
            ft.Row([
                # SETTINGS FIRST HALF MAIN CONTAINER
                ft.Container(content=ft.Column([
                    ft.Row([
                        ft.Icon("settings", color=ft.colors.WHITE60),
                        ft.Text("REQUIRED DATE / TIME FIELDS",
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE70)
                    ], alignment=ft.MainAxisAlignment.START),

                    ft.Container(content=ft.Row([
                        ft.Text("", expand=1),
                        ft.Text("COLUMN", expand=1, size=12,
                                text_align=ft.TextAlign.CENTER),
                        ft.Text("NAME", expand=2, size=12,
                                text_align=ft.TextAlign.CENTER)
                    ]), bgcolor=ft.colors.BLUE_GREY_700,
                        margin=ft.margin.only(0, 5, 0, -10)),

                    # Container for the Required Fields
                    ft.Container(content=ft.Column([
                        FieldContainer(icon="calendar_month", label="Date",
                                       col_ref=self._date_col,
                                       name_ref=self._date_name),
                        FieldContainer(icon="watch_later_outlined",
                                       label="Start\nTime",
                                       col_ref=self._start_time_col,
                                       name_ref=self._start_time_name),
                        FieldContainer(icon="watch_later_rounded",
                                       label="End\nTime",
                                       col_ref=self._end_time_col,
                                       name_ref=self._end_time_name),
                    ], spacing=15),
                    bgcolor=ft.colors.BLUE_GREY_800,
                    padding=ft.padding.all(10))
                ]),
                bgcolor=ft.colors.BLUE_GREY_900,
                expand=1, height=500,
                padding=ft.padding.only(10, 8, 10, 10),
                margin=ft.margin.symmetric(0, 10),
                border_radius=ft.border_radius.all(12)),

                # SETTINGS SECOND HALF MAIN CONTAINER
                ft.Container(content=ft.Column([
                    ft.Row([
                        ft.Icon("settings", color=ft.colors.WHITE60),
                        ft.Text("OTHER SETTINGS", weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE70)
                    ], alignment=ft.MainAxisAlignment.START),

                    ft.Row([
                        ft.ElevatedButton("BACK", height=40,
                                          bgcolor=ft.colors.BLUE_GREY_700,
                                          color=ft.colors.WHITE,
                                          on_click=lambda e: e.page.go("/dashboard")),
                        ft.ElevatedButton("SAVE SETTINGS",
                                          icon="save_rounded", height=40,
                                          bgcolor=ft.colors.BLUE_ACCENT_700,
                                          color=ft.colors.WHITE,
                                          on_click=self.save_settings)
                    ], alignment=ft.MainAxisAlignment.END, spacing=10),
                ]),
                bgcolor=ft.colors.BLUE_GREY_900,
                padding=ft.padding.only(10, 8, 10, 10),
                margin=ft.margin.symmetric(0, 10), expand=1,
                border_radius=ft.border_radius.all(12))

            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=1,
               vertical_alignment=ft.CrossAxisAlignment.START)
        ]

        # Load the existing saved settings.json config
        self.load_settings()

    def save_settings(self, e):
        """ Event for saving the settings to a JSON config file. """
        # Get first the data from the fields
        date_col = self._date_col.current.value
        date_name = self._date_name.current.value
        start_time_col = self._start_time_col.current.value
        start_time_name = self._start_time_name.current.value
        end_time_col = self._end_time_col.current.value
        end_time_name = self._end_time_name.current.value

        # Put it into a dictionary for transforming into a json file
        final_data= {"required": [
            [date_col, date_name],
            [start_time_col, start_time_name],
            [end_time_col, end_time_name]
        ]}

        # Save the dictionary into a json file
        with open(self.settings_path, "w") as outfile:
            outfile.write(json.dumps(final_data))

        # Create the bottom sheet control for displaying succesfull save
        bottom_sheet = ft.BottomSheet(content=ft.Container(
            padding=25,
            content=ft.Column([
                ft.Row([
                    ft.Icon("save_rounded", size=40,
                            color=ft.colors.GREEN_900),
                    ft.Text("Settings has been successfully saved on config folder.",
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE, size=16)
                ]),
                ft.Row([
                    ft.Text("NOTE: Redownload previously added GSheet URLs "
                            "if you changed\nthe column settings to update its "
                            "saved data format accordingly.",
                            italic=True, size=13, color=ft.colors.WHITE70),
                    ft.ElevatedButton(content=ft.Text("OK", color=ft.colors.WHITE),
                                  bgcolor=ft.colors.GREEN_700,
                                  on_click=lambda a: a.page.close(bottom_sheet)),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ], tight=True)
        ), bgcolor=ft.colors.GREEN_ACCENT_700)
        e.page.open(bottom_sheet)

    def load_settings(self):
        """ Loads the saved config settings data to the settings UI. """
        if self.settings_path.exists():
            with open(self.settings_path) as file:
                settings_data = json.loads(file.read())
                # Assign the required fields to its corresponding fields
                required = settings_data["required"]
                self._date_col.current.value = required[0][0]
                self._date_name.current.value = required[0][1]
                self._start_time_col.current.value = required[1][0]
                self._start_time_name.current.value = required[1][1]
                self._end_time_col.current.value = required[2][0]
                self._end_time_name.current.value = required[2][1]


#----------------------------------
# HELPER CLASS FOR FIELD CONTAINER
#----------------------------------
class FieldContainer(ft.Row):

    def __init__(self, *, icon, label, col_ref, name_ref):
        """
        Custom Control for Settings to generate
        a row of field setting with label, icon,
        col field and name field.
        """
        super().__init__()

        self.controls = [
            ft.Row([
                ft.Icon(icon, color=ft.colors.WHITE70),
                ft.Text(label, weight=ft.FontWeight.BOLD)], expand=1),
            ft.TextField(ref=col_ref, hint_text="COL Letter",
                         hint_style=ft.TextStyle(color=ft.colors.BLACK54, size=12),
                         bgcolor=ft.colors.WHITE70,
                         border_color=ft.colors.GREY_500,
                         color=ft.colors.BLACK,
                         text_size=16, expand=1,
                         text_align=ft.TextAlign.CENTER,
                         input_filter=ft.InputFilter(regex_string=r"^[A-Z]*$",
                                                     replacement_string="")),
            ft.TextField(ref=name_ref, hint_text="Data Column Name",
                         hint_style=ft.TextStyle(color=ft.colors.BLACK54, size=12),
                         bgcolor=ft.colors.WHITE70,
                         border_color=ft.colors.GREY_500,
                         color=ft.colors.BLACK,
                         text_size=14, expand=2)
        ]
