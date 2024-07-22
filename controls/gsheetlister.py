# ---------------------------------------------------
# gsheetlister.py - GSheetLister Class
# ---------------------------------------------------
# A custom flet control that manages and shows a
# list of gsheeturl control objects. It is a card
# container that contains a header with filter
# control dropdowns and buttons. The body is also
# a column that lists gsheeturl controls.
# This control autoloads the saved data on the
# current month and year if there is any.
# ---------------------------------------------------

import flet as ft
import json
import time
from pathlib import Path
from datetime import datetime
from calendar import month_name as months
from controls.gsheeturl import GSheetURL
from modules.reader import Reader
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
        self._month_dropdown = ft.Ref[ft.Dropdown]()
        self._year_dropdown = ft.Ref[ft.Dropdown]()
        self._loading_container = ft.Ref[ft.Container]()
        self._progress_ring = ft.Ref[ft.ProgressRing]()
        self._loading_message = ft.Ref[ft.Text]()
        self._loading_icon = ft.Ref[ft.Icon]()

        # Determine the list of months and years to the dropdown
        month_options = [ft.dropdown.Option(text=m, key=str(k).zfill(2))
                         for k, m in enumerate(list(months)[1:], start=1)]
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
                       ref=self._month_dropdown,
                       on_change=self._filter_gsheeturl,
                       bgcolor=ft.colors.BLUE_GREY_700,
                       border_color=ft.colors.BLUE_GREY_600,
                       width=150, height=35, text_size=15,
                       content_padding=ft.padding.symmetric(5, 10),
                       prefix_icon="calendar_month_rounded",
                       value=datetime.now().strftime("%m")),
                    ft.Dropdown(options=year_options,
                       ref=self._year_dropdown,
                       on_change=self._filter_gsheeturl,
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
                                    height=25, width=25,
                                    ref=self._progress_ring),
                    ft.Icon("find_in_page_rounded",
                            size=30, visible=False,
                            color=ft.colors.WHITE54,
                            ref=self._loading_icon),
                    ft.Text("LOADING GSHEETS DATA...",
                            weight=ft.FontWeight.BOLD,
                            ref=self._loading_message)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                   ref=self._loading_container, height=310, visible=False)
            ])
        ])

        # Load the GSheets URL data on initialize depending on current
        # month and year in dropdown. Show the message indicator if
        # not at least 1 gsheet url data is loaded.
        self._load_gsheeturl_data()
        if not len(self._gsheets_url_column.current.controls):
            self._toggle_message_indicator(isloading=False)

    def append(self, gsheeturl):
        """ This method appends a GSheetURL object to its Column List. """
        if gsheeturl:
            self._gsheets_url_column.current.controls.append(gsheeturl)

    def reset(self):
        """ This method clears the list of gsheeturls. """
        self._gsheets_url_column.current.controls.clear()

    def disable_filter_controls(self, flag):
        """ This will toggle to disable or not the filter controls. """
        self._month_dropdown.current.disabled = flag
        self._year_dropdown.current.disabled = flag

    def _toggle_message_indicator(self, *, isloading=False):
        """
        Toggles the loading based on the given parameters:
        visible=True & isloading=True - show loading with progress ring
        visible=True & isloading=False - show icon with not found data message
        visible=False - hide the loading container entirely
        """
        self._loading_container.current.visible = True
        month = self._month_dropdown.current.value
        year = self._year_dropdown.current.value
        visible = isloading
        if not isloading:
            visible = not bool(len(self._gsheets_url_column.current.controls))

        match [visible, isloading]:
            case [True, True]:
                self._progress_ring.current.visible = True
                self._loading_icon.current.visible = False
                self._loading_message.current.value = "LOADING GSHEETS DATA..."
            case [True, False]:
                self._progress_ring.current.visible = False
                self._loading_icon.current.visible = True
                filterstr = datetime.strptime(f"{month} {year}", "%m %Y")
                filterstr = filterstr.strftime("%B %Y").upper()
                message = f"NO GSHEETS DATA SAVED ON {filterstr}"
                self._loading_message.current.value = message
            case [False, False]:
                self._loading_container.current.visible = False

    def _filter_gsheeturl(self, e):
        """
        This callback method will be used by the dropdown to trigger
        loading of new gsheeturl data based on selected month or year.
        """
        # Reset first the existing list of gsheeturls
        self.reset()
        # Show the loading indicator and wait for 1 sec
        self._toggle_message_indicator(isloading=True)
        self.disable_filter_controls(True)
        e.page.update()
        time.sleep(1)
        # Start loading the gsheeturl data based on dropdown values
        self._load_gsheeturl_data()
        # Update the loading container and reset the filter controls
        self._toggle_message_indicator(isloading=False)
        self.disable_filter_controls(False)
        e.page.update()

    def _load_gsheeturl_data(self):
        """
        This method will load json from data folder based on the month
        and year dropdown values. It will create a gsheeturl control
        and cache its loaded data into memory.
        """
        month = self._month_dropdown.current.value
        year = self._year_dropdown.current.value
        data_dir = Path(Reader.BASE_PATH / "downloads/data")

        if not data_dir.exists():
            return  # If data folder does not exist then exit this method

        for path_name in data_dir.iterdir():
            if path_name.name.startswith(f"{month}-{year}"):
                with open(path_name, "r") as file:
                    gsheet_data = json.loads(file.read())
                    gsheet_control = GSheetURL(gsheet_data["url"])
                    self.append(gsheet_control)
                    owner = gsheet_data["owner"]
                    month = gsheet_data["month"]
                    timestamp = gsheet_data["timestamp"]
                    gsheet_control.update_display_labels(
                        owner=owner, month=month, timestamp=timestamp,
                        autoupdate=False)
