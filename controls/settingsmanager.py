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
            ft.Row([
                # First Half Container with Title
                ft.Container(content=ft.Column([
                    ft.Row([
                        ft.Icon("settings", color=ft.colors.WHITE60),
                        ft.Text("REQUIRED DATE / TIME FIELDS",
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE70)
                    ], alignment=ft.MainAxisAlignment.START),

                    # Container for the Required Fields
                    ft.Container(content=ft.Column([
                        ft.Row([  # DATE REQUIRED FIELD
                            ft.Row([
                                ft.Icon("calendar_month", color=ft.colors.WHITE70),
                                ft.Text("Date", weight=ft.FontWeight.BOLD),
                            ], expand=1),
                            ft.TextField(hint_text="COL Letter",
                                         hint_style=ft.TextStyle(
                                             color=ft.colors.BLACK54, size=12),
                                         bgcolor=ft.colors.WHITE70,
                                         border_color=ft.colors.GREY_500,
                                         color=ft.colors.BLACK,
                                         text_size=16, expand=1,
                                         text_align=ft.TextAlign.CENTER,
                                         input_filter=ft.InputFilter(
                                             regex_string=r"^[A-Z]*$",
                                             replacement_string=""
                                         )),
                            ft.TextField(hint_text="Report Column Name",
                                         hint_style=ft.TextStyle(
                                             color=ft.colors.BLACK54, size=12),
                                         bgcolor=ft.colors.WHITE70,
                                         border_color=ft.colors.GREY_500,
                                         color=ft.colors.BLACK,
                                         text_size=14, expand=2)
                        ]),

                        ft.Row([  # START TIME REQUIRED FIELD
                            ft.Row([
                                ft.Icon("watch_later_outlined",
                                        color=ft.colors.WHITE70),
                                ft.Text("Start\nTime",
                                        weight=ft.FontWeight.BOLD),
                            ], expand=1),
                            ft.TextField(hint_text="COL Letter",
                                         hint_style=ft.TextStyle(
                                             color=ft.colors.BLACK54, size=12),
                                         bgcolor=ft.colors.WHITE70,
                                         border_color=ft.colors.GREY_500,
                                         color=ft.colors.BLACK,
                                         text_size=14, expand=1,
                                         input_filter=ft.InputFilter(
                                             regex_string=r"^[A-Z]*$",
                                             replacement_string=""
                                         )),
                            ft.TextField(hint_text="Report Column Name",
                                         hint_style=ft.TextStyle(
                                             color=ft.colors.BLACK54, size=12),
                                         bgcolor=ft.colors.WHITE70,
                                         border_color=ft.colors.GREY_500,
                                         color=ft.colors.BLACK,
                                         text_size=14, expand=2)
                        ]),

                        ft.Row([  # END TIME REQUIRED FIELD
                            ft.Row([
                                ft.Icon("watch_later_rounded",
                                        color=ft.colors.WHITE70),
                                ft.Text("End\nTime",
                                        weight=ft.FontWeight.BOLD),
                            ], expand=1),
                            ft.TextField(hint_text="COL Letter",
                                         hint_style=ft.TextStyle(
                                             color=ft.colors.BLACK54, size=12),
                                         bgcolor=ft.colors.WHITE70,
                                         border_color=ft.colors.GREY_500,
                                         color=ft.colors.BLACK,
                                         text_size=14, expand=1,
                                         input_filter=ft.InputFilter(
                                             regex_string=r"^[A-Z]*$",
                                             replacement_string=""
                                         )),
                            ft.TextField(hint_text="Report Column Name",
                                         hint_style=ft.TextStyle(
                                             color=ft.colors.BLACK54, size=12),
                                         bgcolor=ft.colors.WHITE70,
                                         border_color=ft.colors.GREY_500,
                                         color=ft.colors.BLACK,
                                         text_size=14, expand=2)
                        ])
                    ], spacing=15),
                    bgcolor=ft.colors.BLUE_GREY_800,
                    padding=ft.padding.all(10))
                ]),
                bgcolor=ft.colors.BLUE_GREY_900,
                expand=1, height=500,
                padding=ft.padding.only(10, 8, 10, 10),
                margin=ft.margin.symmetric(0, 10),
                border_radius=ft.border_radius.all(12)),

                # Second Half Container with Title
                ft.Container(content=ft.Row([
                    ft.Icon("settings", color=ft.colors.WHITE60),
                    ft.Text("", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE54),
                    ft.ElevatedButton("Dashboard",
                                      on_click=lambda e: e.page.go("/dashboard"))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=ft.colors.BLUE_GREY_900,
                    padding=ft.padding.only(20, 8, 20, 10),
                    margin=ft.margin.symmetric(0, 10),
                    expand=1,
                    border_radius=ft.border_radius.only(12, 12, 0, 0)),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=1)
        ]
