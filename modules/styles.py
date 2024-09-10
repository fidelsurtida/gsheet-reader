# ---------------------------------------------------
# styles.py - Styles Class
# ---------------------------------------------------
# A static module that contains this applications
# button or control style definitions.
# No need to instantiate this class, just call the
# style references and pass it wherever needed.
# ---------------------------------------------------

import flet as ft
from flet_core.types import ControlState as CState


class Styles:
    """ Contains a list of static control styles. """

    # -------------------
    #  GSHEETURL STYLES
    # -------------------
    download_url_style = ft.ButtonStyle(
        color={
            CState.DEFAULT: ft.colors.GREY_400,
            CState.HOVERED: ft.colors.GREEN_500,
            CState.DISABLED: ft.colors.GREY_700
        }
    )
    remove_url_style = ft.ButtonStyle(
        color={
            CState.DEFAULT: ft.colors.GREY_400,
            CState.HOVERED: ft.colors.RED_400,
            CState.DISABLED: ft.colors.GREY_700
        }
    )

    # ----------------------------
    #  MAIN WINDOW BUTTON STYLES
    # ----------------------------
    add_url_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=8),
        overlay_color={
            CState.PRESSED: ft.colors.GREEN_900
        },
        color={
            CState.DEFAULT: ft.colors.GREEN_900,
            CState.HOVERED: ft.colors.GREEN_100,
            CState.DISABLED: ft.colors.GREY_900
        },
        bgcolor={
            CState.HOVERED: ft.colors.GREEN_300,
            CState.DEFAULT: ft.colors.GREEN_500,
            CState.DISABLED: ft.colors.GREY_800
        }
    )
    settings_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=ft.padding.symmetric(5, 8),
        bgcolor={
            CState.HOVERED: ft.colors.BLUE_GREY_900,
            CState.DEFAULT: ft.colors.BLACK12
        }
    )
    recently_added_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=5),
        color=ft.colors.WHITE38,
        bgcolor={
            CState.DEFAULT: ft.colors.BLACK12
        },
        side={
            CState.DEFAULT: ft.BorderSide(1, ft.colors.BLACK26)
        }
    )
    recently_active_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=5),
        color=ft.colors.DEEP_ORANGE_800,
        bgcolor={
            CState.DEFAULT: ft.colors.ORANGE_ACCENT
        },
        side={
            CState.DEFAULT: ft.BorderSide(3, ft.colors.ORANGE_700)
        }
    )
    download_data_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=10),
        overlay_color={
            CState.PRESSED: ft.colors.BLUE_800
        },
        color={
            CState.DEFAULT: ft.colors.BLUE_900,
            CState.HOVERED: ft.colors.BLUE_100,
            CState.DISABLED: ft.colors.GREY_900
        },
        bgcolor={
            CState.HOVERED: ft.colors.BLUE_400,
            CState.DEFAULT: ft.colors.BLUE_500,
            CState.DISABLED: ft.colors.GREY_800
        }
    )
