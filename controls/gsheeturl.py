# ---------------------------------------------------
# gsheeturl.py - GSheetURL Class
# ---------------------------------------------------
# A class that represents a flet custom control
# for displaying the added GSheet URLs. It shows
# the URL, Last Time Updated, Department Owner of
# the sheet and action buttons for this control.
# ---------------------------------------------------

import flet as ft
import json
from pathlib import Path
from modules.reader import Reader
from controls.progress import Progress
from modules.styles import Styles


class GSheetURL(ft.Container):

    def __init__(self, url, progressbar: Progress):
        """
        Custom Flet Control for displaying an item container of
        added valid GSheet URL. Displays the URL, Timestamp,
        Sheet Owner and action buttons.
        """
        super().__init__()

        # Save the url of the gsheet and the reference to the progressbar
        self.url = url
        self.progressbar = progressbar

        # Declaration of flet control references
        self._owner_name_text = ft.Ref[ft.Text]()
        self._owner_container = ft.Ref[ft.Container]()
        self._month_container = ft.Ref[ft.Container]()
        self._timestamp_container = ft.Ref[ft.Container]()
        self._progress_ring = ft.Ref[ft.ProgressRing]()
        self._completed_icon = ft.Ref[ft.Icon]()
        self._timestamp_text = ft.Ref[ft.Text]()
        self._month_text = ft.Ref[ft.Text]()
        self._redownload_button = ft.Ref[ft.IconButton]()
        self._remove_button = ft.Ref[ft.IconButton]()

        # Initialize first the container parameters
        self.bgcolor = ft.colors.BLUE_GREY_900
        self.border_radius = 5
        self.padding = ft.padding.only(18, 5, 15, 5)

        # Initialize the custom control design UI
        self.content = ft.Row([
            ft.ProgressRing(ref=self._progress_ring, height=20, width=20),
            ft.Icon("file_present_rounded", ref=self._completed_icon,
                    size=30, color=ft.colors.LIGHT_BLUE_300, visible=False),
            ft.Column([
                ft.Row([
                    ft.Icon("insert_link_rounded", size=14),
                    ft.Text(url, width=460,
                            no_wrap=True, tooltip=url,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            color=ft.colors.WHITE60),
                ], spacing=3),
                ft.Row([
                    ft.Container(content=ft.Row([
                        ft.Icon("calendar_month_rounded", size=12,
                                color=ft.colors.WHITE),
                        ft.Text("MONTH: Fetching Details...",
                                ref=self._month_text,
                                color=ft.colors.WHITE, size=11,
                                weight=ft.FontWeight.BOLD)
                        ], spacing=5),
                        ref=self._month_container,
                        bgcolor=ft.colors.GREY_600,
                        padding=ft.padding.symmetric(3, 5), border_radius=5),

                    ft.Container(content=ft.Row([
                        ft.Icon("timer_outlined", size=12,
                                color=ft.colors.WHITE),
                        ft.Text("TIMESTAMP: Fetching Details...",
                                ref=self._timestamp_text,
                                size=11, color=ft.colors.WHITE,
                                weight=ft.FontWeight.BOLD)
                        ], spacing=5),
                        ref=self._timestamp_container,
                        bgcolor=ft.colors.GREY_600,
                        padding=ft.padding.symmetric(3, 5), border_radius=5)
                ], spacing=8)
            ], spacing=3),
            ft.Row([
                ft.Container(ft.Text("PENDING", ref=self._owner_name_text,
                                     max_lines=2, width=150, size=13,
                                     text_align=ft.TextAlign.CENTER,
                                     weight=ft.FontWeight.BOLD),
                             ref=self._owner_container,
                             bgcolor=ft.colors.GREY_700,
                             border_radius=6,
                             padding=ft.padding.symmetric(3, 10),
                             margin=ft.margin.only(0, 0, 20, 0)),
                ft.IconButton(icon="download_for_offline_rounded",
                              ref=self._redownload_button,
                              on_click=self.redownload_gsheet_data,
                              style=Styles.download_url_style,
                              tooltip="DOWNLOAD DATA", disabled=True),
                ft.IconButton(icon="delete_forever",
                              ref=self._remove_button,
                              style=Styles.remove_url_style,
                              tooltip="REMOVE URL", disabled=True)
            ], spacing=1)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def update_display_labels(self, *, owner, month, timestamp,
                              autoupdate=True, diskload=True):
        """
        This method will be used to update the display fields of this
        control. Department Owner, Timestamp and status icon.
        """
        self._owner_name_text.current.value = owner
        self._owner_container.current.bgcolor = ft.colors.LIGHT_BLUE_800
        self._month_container.current.bgcolor = ft.colors.LIGHT_BLUE_700
        self._timestamp_container.current.bgcolor = ft.colors.LIGHT_BLUE_700
        self._progress_ring.current.visible = False
        self._completed_icon.current.visible = True
        self._timestamp_text.current.value = f"TIMESTAMP: {timestamp}"
        self._month_text.current.value = month
        self._remove_button.current.disabled = False
        self._redownload_button.current.disabled = False

        # Update only this control if specified, specify false on app load
        # If autoupdate, change the completed icon to check, else a file
        if not diskload:
            self._completed_icon.current.name = "check_circle_rounded"
            self._completed_icon.current.color = ft.colors.GREEN
            self._owner_container.current.bgcolor = ft.colors.TEAL_800
            self._month_container.current.bgcolor = ft.colors.TEAL_600
            self._timestamp_container.current.bgcolor = ft.colors.TEAL_600
        if autoupdate:
            self.update()

    def reset_display_labels(self):
        """ This method resets the labels to its starting UI gray design. """
        self._owner_name_text.current.value = "PENDING"
        self._owner_container.current.bgcolor = ft.colors.GREY_700
        self._month_container.current.bgcolor = ft.colors.GREY_600
        self._timestamp_container.current.bgcolor = ft.colors.GREY_600
        self._progress_ring.current.visible = True
        self._completed_icon.current.visible = False
        self._timestamp_text.current.value = "TIMESTAMP: Fetching Details..."
        self._month_text.current.value = "MONTH: Fetching Details..."
        self._remove_button.current.disabled = True
        self._redownload_button.current.disabled = True
        self.update()

    def redownload_gsheet_data(self, e):
        """ Redownload the data and save it again as json data file. """
        self.reset_display_labels()

        def fetch_completed(**kwargs):
            """ Callback method after the data fetch has been completed. """
            self.update_display_labels(owner=kwargs["owner"],
                                       month=kwargs["month"],
                                       timestamp=kwargs["timestamp"],
                                       diskload=True)

            # Save the downloaded data to its own JSON file
            data_dir = Path(Reader.BASE_PATH / "downloads/data")
            owner_formatted = kwargs["owner"].lower().replace(" ", "-")
            filename = f"{kwargs["month_num"]}-{owner_formatted}.json"
            file = data_dir / filename
            with open(file, "w") as outfile:
                json.dump(kwargs, outfile)

        def progress_callback(**kwargs):
            """ Callback for the progress bar control to update. """
            self.progressbar.update_progress(**kwargs)

        # Create Reader class to fetch data and pass the required callbacks
        reader = Reader(url=self.url)
        result = reader.fetch_data(sheet_identifier="*-",
                                   progress=progress_callback,
                                   completed=fetch_completed)