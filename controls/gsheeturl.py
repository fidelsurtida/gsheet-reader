# ---------------------------------------------------
# gsheeturl.py - GSheetURL Class
# ---------------------------------------------------
# A class that represents a flet custom control
# for displaying the added GSheet URLs. It shows
# the URL, Last Time Updated, Department Owner of
# the sheet and action buttons for this control.
# ---------------------------------------------------

import flet as ft
from modules.styles import Styles


class GSheetURL(ft.Container):

    def __init__(self, url):
        """
        Custom Flet Control for displaying an item container of
        added valid GSheet URL. Displays the URL, Timestamp,
        Sheet Owner and action buttons.
        """
        super().__init__()

        # Declaration of flet control references
        self._owner_name_text = ft.Ref[ft.Text]()
        self._owner_container = ft.Ref[ft.Container]()
        self._month_container = ft.Ref[ft.Container]()
        self._timestamp_container = ft.Ref[ft.Container]()
        self._progress_ring = ft.Ref[ft.ProgressRing]()
        self._completed_icon = ft.Ref[ft.Icon]()
        self._timestamp_text = ft.Ref[ft.Text]()
        self._month_text = ft.Ref[ft.Text]()
        self._download_button = ft.Ref[ft.IconButton]()
        self._remove_button = ft.Ref[ft.IconButton]()

        # Initialize first the container parameters
        self.bgcolor = ft.colors.BLUE_GREY_900
        self.border_radius = 5
        self.padding = ft.padding.only(18, 5, 15, 5)

        # Initialize the custom control design UI
        self.content = ft.Row([
            ft.ProgressRing(ref=self._progress_ring, height=20, width=20),
            ft.Icon("check_circle_rounded", ref=self._completed_icon,
                    size=30, color=ft.colors.GREEN, visible=False),
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
                              ref=self._download_button,
                              style=Styles.download_url_style,
                              tooltip="DOWNLOAD DATA", disabled=True),
                ft.IconButton(icon="delete_forever",
                              ref=self._remove_button,
                              style=Styles.remove_url_style,
                              tooltip="REMOVE URL", disabled=True)
            ], spacing=1)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def update_display_labels(self, *, owner, month, timestamp,
                              autoupdate=True):
        """
        This method will be used to update the display fields of this
        control. Department Owner, Timestamp and status icon.
        """
        self._owner_name_text.current.value = owner
        self._owner_container.current.bgcolor = ft.colors.TEAL_800
        self._month_container.current.bgcolor = ft.colors.TEAL_600
        self._timestamp_container.current.bgcolor = ft.colors.TEAL_600
        self._progress_ring.current.visible = False
        self._completed_icon.current.visible = True
        self._timestamp_text.current.value = f"TIMESTAMP: {timestamp}"
        self._month_text.current.value = month
        self._remove_button.current.disabled = False
        self._download_button.current.disabled = False
        # Update only this control if specified, specify false on app load
        if autoupdate:
            self.update()
