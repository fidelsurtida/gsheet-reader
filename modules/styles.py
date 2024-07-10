# ---------------------------------------------------
# styles.py - Styles Class
# ---------------------------------------------------
# A static module that contains this applications
# button or control style definitions.
# No need to instantiate this class, just call the
# style references and pass it wherever needed.
# ---------------------------------------------------

import flet as ft


class Styles:
    """ Contains a list of static control styles. """

    # -------------------
    #  GSHEETURL STYLES
    # -------------------
    download_url_style = ft.ButtonStyle(
        color={
            ft.ControlState.DEFAULT: ft.colors.GREY_400,
            ft.ControlState.HOVERED: ft.colors.GREEN_500,
            ft.ControlState.DISABLED: ft.colors.GREY_700
        }
    )
    remove_url_style = ft.ButtonStyle(
        color={
            ft.ControlState.DEFAULT: ft.colors.GREY_400,
            ft.ControlState.HOVERED: ft.colors.RED_400,
            ft.ControlState.DISABLED: ft.colors.GREY_700
        }
    )

    # ----------------------------
    #  MAIN WINDOW BUTTON STYLES
    # ----------------------------
    add_url_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=8),
        overlay_color={
            ft.ControlState.PRESSED: ft.colors.GREEN_900
        },
        color={
            ft.ControlState.DEFAULT: ft.colors.GREEN_900,
            ft.ControlState.HOVERED: ft.colors.GREEN_100,
            ft.ControlState.DISABLED: ft.colors.GREY_900
        },
        bgcolor={
            ft.ControlState.HOVERED: ft.colors.GREEN_300,
            ft.ControlState.DEFAULT: ft.colors.GREEN_500,
            ft.ControlState.DISABLED: ft.colors.GREY_800
        }
    )
    settings_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=ft.padding.symmetric(5, 8),
        bgcolor={
            ft.ControlState.HOVERED: ft.colors.BLUE_GREY_900,
            ft.ControlState.DEFAULT: ft.colors.BLACK12
        }
    )
    download_data_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=10),
        overlay_color={
            ft.ControlState.PRESSED: ft.colors.BLUE_800
        },
        color={
            ft.ControlState.DEFAULT: ft.colors.BLUE_900,
            ft.ControlState.HOVERED: ft.colors.BLUE_100,
            ft.ControlState.DISABLED: ft.colors.GREY_900
        },
        bgcolor={
            ft.ControlState.HOVERED: ft.colors.BLUE_400,
            ft.ControlState.DEFAULT: ft.colors.BLUE_500,
            ft.ControlState.DISABLED: ft.colors.GREY_800
        }
    )
