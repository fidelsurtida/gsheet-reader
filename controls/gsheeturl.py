# ---------------------------------------------------
# gsheeturl.py - GSheetURL Class
# ---------------------------------------------------
# A class that represents a flet custom control
# for displaying the added GSheet URLs. It shows
# the URL, Last Time Updated, Department Owner of
# the sheet and action buttons for this control.
# ---------------------------------------------------

import flet as ft


class GSheetURL(ft.Container):

    def __init__(self, url):
        """
        Custom Flet Control for displaying an item container of
        added valid GSheet URL. Displays the URL, Timestamp,
        Sheet Owner and action buttons.
        """
        super().__init__()

        # Initialize first the container parameters
        self.bgcolor = ft.colors.BLUE_GREY_900
        self.border_radius = 5
        self.padding = ft.padding.only(18, 5, 15, 5)

        # Initialize the custom control design UI
        self.content = ft.Row([
            ft.ProgressRing(height=20, width=20),
            ft.Column([
                ft.Row([
                    ft.Icon("insert_link_rounded", size=14),
                    ft.Text(url, width=460,
                            no_wrap=True, tooltip=url,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            color=ft.colors.WHITE60),
                ], spacing=3),
                ft.Row([
                    ft.Icon("timer_outlined", size=12),
                    ft.Text("LAST UPDATE: Fetching Details...",
                            size=10, color=ft.colors.WHITE54,
                            weight=ft.FontWeight.BOLD)
                ], spacing=5)
            ], spacing=3),
            ft.Row([
                ft.Container(ft.Text("PENDING", max_lines=1, width=150,
                                     text_align=ft.TextAlign.CENTER,
                                     weight=ft.FontWeight.BOLD),
                             bgcolor=ft.colors.GREY_600,
                             border_radius=6,
                             padding=ft.padding.symmetric(3, 10),
                             margin=ft.margin.only(0, 0, 20, 0)),
                ft.IconButton(icon="download_for_offline_rounded",
                              style=update_url_style,
                              tooltip="DOWNLOAD DATA"),
                ft.IconButton(icon="delete_forever",
                              style=remove_url_style,
                              tooltip="REMOVE URL")
            ], spacing=1)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)


# ----------------------
#  CLASS BUTTON STYLES
# ----------------------
update_url_style = ft.ButtonStyle(
    color={
        ft.ControlState.DEFAULT: ft.colors.GREY_400,
        ft.ControlState.HOVERED: ft.colors.GREEN_500,
        ft.ControlState.DISABLED: ft.colors.GREY_600
    }
)

remove_url_style = ft.ButtonStyle(
    color={
        ft.ControlState.DEFAULT: ft.colors.GREY_400,
        ft.ControlState.HOVERED: ft.colors.RED_400,
        ft.ControlState.DISABLED: ft.colors.GREY_600
    }
)