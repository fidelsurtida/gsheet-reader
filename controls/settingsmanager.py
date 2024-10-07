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
                                          color=ft.colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.END, spacing=10),
                ]),
                bgcolor=ft.colors.BLUE_GREY_900,
                padding=ft.padding.only(10, 8, 10, 10),
                margin=ft.margin.symmetric(0, 10), expand=1,
                border_radius=ft.border_radius.all(12))

            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=1,
               vertical_alignment=ft.CrossAxisAlignment.START)
        ]


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
