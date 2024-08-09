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

    # Class Variable to track Recents and URLs List
    RECENTS = []
    URLS_DB = {}

    def __init__(self, progress_control):
        """
        Custom Flet Control for displaying a list of
        GSheetURL Objects. It contains filter controls
        to manage showing of gsheets according to
        specified date. Contains methods to change and
        clear gsheet list.
        """
        super().__init__()

        # Save the reference of the progressbar control
        self._progressbar = progress_control

        # Declaration of Flet Control References
        self._gsheets_url_column = ft.Ref[ft.Column]()
        self._month_dropdown = ft.Ref[ft.Dropdown]()
        self._year_dropdown = ft.Ref[ft.Dropdown]()
        self._loading_container = ft.Ref[ft.Container]()
        self._progress_ring = ft.Ref[ft.ProgressRing]()
        self._loading_message = ft.Ref[ft.Text]()
        self._loading_icon = ft.Ref[ft.Icon]()
        self._recent_button = ft.Ref[ft.ElevatedButton]()

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
                       ref=self._recent_button,
                       on_click=lambda e: self.show_recently_added(),
                       icon="new_releases_rounded",
                       style=Styles.recently_added_style,
                       height=35),
                    ft.Dropdown(options=month_options,
                       ref=self._month_dropdown,
                       on_change=lambda e: self.filter_gsheeturl(),
                       bgcolor=ft.colors.BLUE_GREY_700,
                       border_color=ft.colors.BLUE_GREY_600,
                       width=150, height=35, text_size=15,
                       content_padding=ft.padding.symmetric(5, 10),
                       prefix_icon="calendar_month_rounded",
                       value=datetime.now().strftime("%m")),
                    ft.Dropdown(options=year_options,
                       ref=self._year_dropdown,
                       on_change=lambda e: self.filter_gsheeturl(),
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
        self._load_gsheeturl_data(initial_load=True)
        if not len(self._gsheets_url_column.current.controls):
            self._toggle_message_indicator(isloading=False)

    def append(self, gsheeturl, first=False):
        """ This method appends a GSheetURL object to its Column List. """
        if gsheeturl:
            if first:
                self._gsheets_url_column.current.controls.insert(0, gsheeturl)
            else:
                self._gsheets_url_column.current.controls.append(gsheeturl)

    def remove(self, gsheeturl):
        """ This method removes a specific GSheetURL object to its list. """
        if gsheeturl:
            self._gsheets_url_column.current.controls.remove(gsheeturl)

    def add_recents(self, filename):
        """
        This method will be used to add a recently saved file name to
        the recents list. It will also make sure to save only latest
        ten items of unique urls added.
        """
        self.RECENTS.insert(0, filename)
        self.RECENTS = self.RECENTS[:10]
        # Save the current RECENTS into a JSON file
        file = Path(Reader.BASE_PATH / "downloads/data/recents.json")
        with open(file, "w") as outfile:
            json.dump(self.RECENTS, outfile)

    def add_urlsdb(self, *, url, month, month_num, year, owner):
        """
        This method adds gsheet url data from currently finished fetch
        callback method in main. It should be used only for newly added urls.
        """
        if url not in self.URLS_DB.keys():
            self.URLS_DB[url] = {"month": month, "month_num": month_num,
                                 "year": year, "owner": owner}

    def reset(self):
        """ This method clears the list of gsheeturls. """
        self._gsheets_url_column.current.controls.clear()

    def disable_filter_controls(self, flag):
        """ This will toggle to disable or not the filter controls. """
        self._month_dropdown.current.disabled = flag
        self._year_dropdown.current.disabled = flag
        self._recent_button.current.disabled = flag

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

    def filter_gsheeturl(self, month=None, year=None):
        """
        This callback method will be used by the dropdown to trigger
        loading of new gsheeturl data based on selected month or year.
        It can also be called outside to update this Gsheetlister control
        the specified current month and year filters.
        """
        # If there is a supplied month and year parameter then change
        # the dropdown values to it
        if month:
            self._month_dropdown.current.value = month
        if year:
            self._year_dropdown.current.value = year

        # Reset first the existing list of gsheeturls
        self.reset()
        # Show the loading indicator and wait for 1 sec
        self._toggle_message_indicator(isloading=True)
        self.disable_filter_controls(True)
        self.update()
        time.sleep(1)
        # Start loading the gsheeturl data based on dropdown values
        self._load_gsheeturl_data()
        # Update the loading container and reset the filter controls
        self._toggle_message_indicator(isloading=False)
        self.disable_filter_controls(False)
        self._recent_button.current.style = Styles.recently_added_style
        self.update()

    def _load_gsheeturl_data(self, initial_load=False):
        """
        This method will load json from data folder based on the month
        and year dropdown values. It will create a gsheeturl control
        and cache its loaded data into memory.
        This will also load the recents.json file and also list all
        the existing URLS in the data folder.
        """
        month = self._month_dropdown.current.value
        year = self._year_dropdown.current.value
        data_dir = Path(Reader.BASE_PATH / "downloads/data")

        if not data_dir.exists():
            return  # If data folder does not exist then exit this method

        # Create a gsheeturl control if there are existing urls on this month
        for path_name in data_dir.iterdir():
            if path_name.name.startswith(f"{month}-{year}"):
                self._create_gsheeturl_control(path_name.name, diskload=True)

        # If it's initial load then recreate the URLS_DB dictionary
        # Load also the recents.json file into RECENTS list variable
        if initial_load:
            for path_name in data_dir.iterdir():
                if not path_name.name.startswith("recents"):
                    with open(path_name, "r") as file:
                        url_data = json.loads(file.read())
                        month_str, year_str = url_data["month"].split()
                        month_num = url_data["month_num"].split("-")[0]
                        self.add_urlsdb(url=url_data["url"], month=month_str,
                                        month_num=month_num, year=year_str,
                                        owner=url_data["owner"])

            recents_file = data_dir / "recents.json"
            if recents_file.exists():
                with open(recents_file) as file:
                    self.RECENTS = json.loads(file.read())

    def show_recently_added(self):
        """
        This method will be used by the recently added button to show
        a list of gsheeturls from the recent.json which shows the
        latest top 10 added urls.
        """
        # Reset first the existing list of gsheeturls
        self.reset()
        # Show the loading indicator and wait for 1 sec
        self._toggle_message_indicator(isloading=True)
        self.disable_filter_controls(True)
        self._recent_button.current.style = Styles.recently_active_style
        self.update()
        time.sleep(1)

        # Load and create the gsheeturl controls from RECENTS list
        for filename in self.RECENTS:
            self._create_gsheeturl_control(filename, diskload=False)

        # Update the loading container and reset the filter controls
        self._loading_container.current.visible = False
        self.disable_filter_controls(False)
        self.update()

    def _create_gsheeturl_control(self, filename, diskload):
        """ Helper method to create a gsheeturl control from filename. """
        data_dir = Path(Reader.BASE_PATH / "downloads/data")
        if data_dir.exists():
            with open((data_dir / filename), "r") as file:
                gsheet_data = json.loads(file.read())
                gsheet_control = GSheetURL(gsheet_data["url"],
                                           self._progressbar)
                self.append(gsheet_control)
                owner = gsheet_data["owner"]
                month = gsheet_data["month"]
                timestamp = gsheet_data["timestamp"]
                gsheet_control.update_display_labels(
                    owner=owner, month=month, timestamp=timestamp,
                    autoupdate=False, diskload=diskload)
