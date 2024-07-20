# ---------------------------------------------------
# gsheetlister.py - GSheetLister Class
# ---------------------------------------------------
# A custom flet control that manages and shows a
# list of gsheeturl control objects. It is a card
# container that contains a header with filter
# control dropdowns and buttons. The body is also
# a column that lists gsheeturl controls.
# ---------------------------------------------------

import flet as ft
from datetime import datetime
from calendar import month_name as months
from modules.styles import Styles


class GSheetLister(ft.Card):

    def __init__(self):
        """
        Custom Flet Control for displaying a list of
        GSheetURL Objects. It contains filter controls
        to manage showing of gsheets according to
        specified date. Contains methods to change and
        clear gsheet list.
        """
        super().__init__()

        # Declaration of Flet Control References
        self._gsheets_url_column = ft.Ref[ft.Column]()

        # Determine the list of months and years to the dropdown
        month_options = [ft.dropdown.Option(m) for m in list(months)[1:]]
        cur_year = int(datetime.now().strftime("%Y"))
        year_options = [year for year in range(cur_year, cur_year - 6, -1)]
        year_options = [ft.dropdown.Option(str(y)) for y in year_options]

        # Initialize the custom control design UI
        self.height = 410
        self.content = ft.Column([
            ft.Container(content=ft.Row([
                ft.Row([
                    ft.Icon("event_note_rounded",
                            color=ft.colors.WHITE60),
                    ft.Text("GSHEETS SAVED URLS",
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE54)
                ]),
                ft.Row([
                    ft.ElevatedButton(text="Recently Added",
                       icon="new_releases_rounded",
                       style=Styles.recently_added_style,
                       height=35),
                    ft.Dropdown(options=month_options,
                       bgcolor=ft.colors.BLUE_GREY_700,
                       border_color=ft.colors.BLUE_GREY_600,
                       width=150, height=35, text_size=15,
                       content_padding=ft.padding.symmetric(5, 10),
                       prefix_icon="calendar_month_rounded",
                       value=datetime.now().strftime("%B")),
                    ft.Dropdown(options=year_options,
                       bgcolor=ft.colors.BLUE_GREY_700,
                       border_color=ft.colors.BLUE_GREY_600,
                       width=90, height=35, text_size=15,
                       content_padding=ft.padding.symmetric(5, 10),
                       value=datetime.now().strftime("%Y"))
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
               bgcolor=ft.colors.BLUE_GREY_900,
               padding=ft.padding.only(20, 8, 20, 10),
               border_radius=ft.border_radius.only(12, 12, 0, 0)),

            ft.Stack([
                ft.Container(content=ft.Column([],
                             ref=self._gsheets_url_column, spacing=15,
                             scroll=ft.ScrollMode.AUTO, height=310),
                             padding=ft.padding.all(10),
                             margin=ft.margin.only(5, 0, 5, 0),
                             border_radius=5),

                ft.Container(content=ft.Row([
                    ft.ProgressRing(color=ft.colors.WHITE54,
                                    height=30, width=30),
                    ft.Text("LOADING GSHEETS DATA...",
                            weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                   height=310, visible=False)
            ])
        ])

    def append(self, gsheeturl):
        """
        This method appends a GSheetURL object to its Column List.
        """
        if gsheeturl:
            self._gsheets_url_column.current.controls.append(gsheeturl)
