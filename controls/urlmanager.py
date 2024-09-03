# ---------------------------------------------------
# urlmanager.py - URLManager Class
# ---------------------------------------------------
# A custom flet control that manages the added
# urls and validates them. It shows dialog boxes
# which contain error messages to the related URL.
# This also fetches the gsheet data on a valid
# URL input and converts them to gsheeturl controls.
# ---------------------------------------------------

import flet as ft
import json
import gspread.exceptions as gexceptions
from pathlib import Path
from controls.gsheeturl import GSheetURL
from modules.reader import Reader
from modules.styles import Styles


class URLManager(ft.Card):

    def __init__(self):
        """
        Custom Flet Control for Managing the added URLs.
        It will show respective error dialog boxes on
        invalid URLS and will convert valid into
        gsheeturl controls and add it to gsheetlister.
        """
        super().__init__()

        # Declaration of Flet Control References
        self._gsheet_url = ft.Ref[ft.TextField]()
        self._add_url_button = ft.Ref[ft.ElevatedButton]()

        # Initialize the Custom UI Design
        hint = "https://docs.google.com/spreadsheets/..."
        self.content = ft.Container(
            content=ft.Row([
                ft.TextField(ref=self._gsheet_url,
                             label="Google Sheet URL:",
                             border_color=ft.colors.GREY_500,
                             hint_text=hint,
                             expand=4),
                ft.ElevatedButton(ref=self._add_url_button,
                                  text="ADD URL",
                                  icon="add_link_sharp", height=50,
                                  expand=1,
                                  style=Styles.add_url_style,
                                  on_click=self._add_url_button_event),
                ft.OutlinedButton(content=ft.Icon("settings_rounded",
                                  size=30, color=ft.colors.WHITE60),
                                  width=55, height=50,
                                  style=Styles.settings_style,
                                  tooltip="DATA SETTINGS ")
            ], spacing=15), padding=20)

    def _add_url_button_event(self, e):
        """
        This button event will add a GSheetURL control to
        the container UI interface and perform a data
        fetch on the Google Sheet.
        """
        url = self._gsheet_url.current.value
        gsheetlister = e.page.get_gsheetlister()
        dialogbox = None

        # Perform a validation if the URL given is valid and not empty
        if not url or not url.startswith("https://docs.google.com/"):
            message = ("Google Sheet URL should start with a google\n"
                       "domain, must be a valid URL and not empty.")
            dialogbox = self._generate_invalid_url_dialogbox(message)

        # Perform a validation to determine if URL already exists
        elif url in gsheetlister.URLS_DB.keys():
            data = gsheetlister.URLS_DB[url]
            dialogbox = self._generate_existing_url_dialogbox(gsheetlister,
                                                              data)

        # If dialogbox variable exists then validation fails, we should
        # show the dialog and exit this method immediately
        if dialogbox:
            self._gsheet_url.current.value = ""
            e.page.open(dialogbox)
            e.page.update()
            return

        # Trigger first the recently added event to load recents list
        gsheetlister.show_recently_added()

        # Create a GSheetURL control and append it to the gsheets cont
        gsheeturl_control = GSheetURL(url)
        self._gsheet_url.current.value = ""
        gsheetlister.append(gsheeturl_control, first=True)
        e.page.disable_all_buttons(True)
        e.page.get_progressbar().reset()
        e.page.update()

        def fetch_completed(**kwargs):
            """ Callback method after the data fetch has been completed. """
            gsheeturl_control.update_display_labels(
                owner=kwargs["owner"], month=kwargs["month"],
                timestamp=kwargs["timestamp"], diskload=False)
            # Update the states of UI Controls
            e.page.disable_all_buttons(False)
            e.page.update()

            # Save the downloaded data to its own JSON file
            data_dir = Path(Reader.BASE_PATH / "downloads/data")
            data_dir.mkdir(parents=True, exist_ok=True)
            owner_formatted = kwargs["owner"].lower().replace(" ", "-")
            filename = f"{kwargs['month_num']}-{owner_formatted}.json"
            file = data_dir / filename
            with open(file, "w") as outfile:
                json.dump(kwargs, outfile)

            # Save to the gsheetlister RECENTS list
            gsheetlister.add_recents(filename)
            # Save to the gsheetlister URLS_DB dictionary
            month, year = kwargs["month"].split()
            month_num = kwargs["month_num"].split("-")[0]
            gsheetlister.add_urlsdb(url=kwargs["url"], month=month,
                                    year=year, month_num=month_num,
                                    owner=kwargs["owner"],
                                    filename=filename)

        def progress_callback(**kwargs):
            """ Callback for the progress bar control to update. """
            progressbar_control = e.page.get_progressbar()
            progressbar_control.update_progress(**kwargs)

        # Create Reader class to fetch data and pass the required callbacks
        # If it returns an exception from gspread then show an appropriate
        # error dialog box.
        reader = Reader(url=url)
        result = reader.fetch_data(sheet_identifier="*-",
                                   progress=progress_callback,
                                   completed=fetch_completed)
        reset_prog = True
        match result:
            case gexceptions.SpreadsheetNotFound:
                message = "Spreadsheet not found on the provided URL."
            case gexceptions.APIError:
                message = "API Key Configuration Not Found."
            case gexceptions.GSpreadException:
                message = ("GSheet URL is not shared to the configured\n"
                           "email of GSheet Reader API key.")
            case _:
                reset_prog = False
                message = ("Data Reading Failed. Details of the Error: \n"
                           f"{str(result)}")

        # Remove the gsheeturl control if an exception is found.
        # Also reset the progress and the filter buttons.
        if result is not True:
            dialogbox = self._generate_invalid_url_dialogbox(message)
            e.page.open(dialogbox)
            gsheetlister.remove(gsheeturl_control)
            e.page.disable_all_buttons(False)
            if reset_prog:
                e.page.get_progressbar().reset()
            e.page.update()

    def disable_buttons(self, flag: bool):
        """ Helper method to change state this control buttons. """
        self._add_url_button.current.disabled = flag

    @staticmethod
    def _generate_existing_url_dialogbox(gsheetlister, data):
        """ Helper method to generate an alert dialog for existing urls. """
        def proceed_event(ev):
            # Callback event for the proceed button
            ev.page.close(alert_dialog)
            gsheetlister.filter_gsheeturl(month=data["month_num"],
                                          year=data["year"])

        alert_dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Icon("warning_rounded", color=ft.colors.ORANGE_ACCENT,
                        size=32),
                ft.Text("GSHEET URL EXISTS", weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER, size=20)], spacing=10),
            content=ft.Text(f"This URL is for {data['owner'].upper()}"
                            f" that is added on {data['month']} "
                            f"{data['year']}.\nWould you like to view the "
                            f"saved GSheet URL?"),
            actions=[
                ft.TextButton("Cancel",
                              on_click=lambda a: a.page.close(alert_dialog)),
                ft.ElevatedButton("Proceed", on_click=proceed_event,
                                  bgcolor=ft.colors.BLUE_ACCENT,
                                  color=ft.colors.WHITE)],
            modal=True, bgcolor=ft.colors.GREY_900)

        return alert_dialog

    @staticmethod
    def _generate_invalid_url_dialogbox(message):
        """ Helper method to generate an alert dialog for empty urls. """
        alert_dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Icon("warning_rounded", color=ft.colors.RED_ACCENT, size=32),
                ft.Text("INVALID GSHEET URL", weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER, size=20)], spacing=10),
            content=ft.Text(message),
            actions=[ft.TextButton("OK",
                     on_click=lambda a: a.page.close(alert_dialog))],
            modal=True, bgcolor=ft.colors.GREY_900)

        return alert_dialog
