import flet as ft
from controls.urlmanager import URLManager
from controls.gsheetlister import GSheetLister
from controls.progress import Progress
from modules.reader import Reader
from modules.styles import Styles


# GLOBAL DATA VARIABLE for creating CSV
DATA = {}

# Flet Control References
download_button = ft.Ref[ft.ElevatedButton]()

# Custom Control References
gsheetlister_control = GSheetLister()
progressbar_control = Progress()
urlmanager_control = URLManager(gsheetlister_control=gsheetlister_control,
                                progress_control=progressbar_control,
                                download_btn=download_button)


def download_button_event():
    """
    This button event will create a csv report based
    on the saved url data json files.
    """
    if DATA:
        download_button.current.disabled = True
        download_button.current.update()
        Reader.generate_csv_report(DATA)
        download_button.current.disabled = False
        download_button.current.update()


# --------------------------------
# FLET MAIN FUNCTION ENTRY POINT
# --------------------------------
def main(page: ft.Page):

    # Set the Window Properties
    page.title = "GSheet Reader"
    page.window.width = 900
    page.window.height = 650
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK

    # Download Button and Progress Bar Container
    download_progress_container = ft.Container(
        content=ft.Row([
            progressbar_control,
            ft.ElevatedButton(
                ref=download_button,
                text="GENERATE CSV",
                icon="save_rounded",
                on_click=download_button_event,
                expand=2, height=50,
                style=Styles.download_data_style)
            ], spacing=30
        ), height=70, padding=10)

    # Add the main elements of the application
    page.add(urlmanager_control)
    page.add(gsheetlister_control)
    page.add(download_progress_container)


# Run the main Flet Window App
ft.app(main)
