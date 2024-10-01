import flet as ft
from controls.urlmanager import URLManager
from controls.settingsmanager import SettingsManager
from controls.gsheetlister import GSheetLister
from controls.progress import Progress
from modules.reader import Reader
from modules.styles import Styles


# Flet Control References
download_button = ft.Ref[ft.ElevatedButton]()

# Custom Control References
progressbar_control = Progress()
gsheetlister_control = GSheetLister()
urlmanager_control = URLManager()


def download_button_event(e):
    """
    This button event will create a csv report based
    on the saved json files.
    """
    # Disable the current visible buttons
    disable_all_buttons(True)
    e.page.update()
    # Generate the CSV Report
    Reader.generate_csv_report(progressbar_control)
    # Enable again all the visible buttons
    disable_all_buttons(False)
    e.page.update()


def disable_all_buttons(flag: bool):
    """ Helper method of the main window to enable/disable all buttons. """
    urlmanager_control.disable_buttons(flag)
    gsheetlister_control.disable_filter_controls(flag)
    gsheetlister_control.disable_gsheeturl_controls(flag)
    download_button.current.disabled = flag


# --------------------------------
# FLET MAIN FUNCTION ENTRY POINT
# --------------------------------
def main(page: ft.Page):

    # Set the Window Properties
    page.window.width = 900
    page.window.height = 650
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK

    # Set function call references on page to easily get parent controls
    page.get_progressbar = lambda: progressbar_control
    page.get_gsheetlister = lambda: gsheetlister_control
    page.get_urlmanager = lambda: urlmanager_control
    page.disable_all_buttons = disable_all_buttons

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

    # Add the root page dashboard to the views
    dashboard_view = ft.View("/dashboard", [
        urlmanager_control,
        gsheetlister_control,
        download_progress_container
    ])
    page.views.clear()
    page.views.append(dashboard_view)

    # Create a route change event to switch between dashboard and settings view
    def route_change(e):
        if e.route == "/dashboard":
            page.views.clear()
            page.views.append(dashboard_view)
            page.title = "GSheet Reader - Dashboard"
        elif e.route == "/settings":
            page.title = "GSheet Reader - Settings"
            page.views.append(ft.View("/settings", [SettingsManager()]))
        page.update()

    # Set the route change event and default go to the dashboard page
    page.on_route_change = route_change
    page.go("/dashboard")


# Run the main Flet Window App
ft.app(main)
