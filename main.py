import flet as ft
import json
from pathlib import Path
from controls.gsheeturl import GSheetURL
from controls.gsheetlister import GSheetLister
from controls.progress import Progress
from modules.reader import Reader
from modules.styles import Styles


# GLOBAL DATA VARIABLE for creating CSV
DATA = {}

# Flet Control References
gsheet_url = ft.Ref[ft.TextField]()
download_button = ft.Ref[ft.ElevatedButton]()
add_url_button = ft.Ref[ft.ElevatedButton]()

# Custom Control References
gsheetlister_control = GSheetLister()
progressbar_control = Progress()


def add_url_button_event(e):
    """
    This button event will add a GSheetURL control to
    the container UI interface and perform a data
    fetch on the Google Sheet.
    """
    url = gsheet_url.current.value

    # Perform a validation first on the url if it exists already on data
    if url in gsheetlister_control.URLS_DB.keys():
        data = gsheetlister_control.URLS_DB[url]

        def proceed_event(ev):
            ev.page.close(dlg)
            gsheetlister_control.filter_gsheeturl(month=data["month_num"],
                                                  year=data["year"])

        dlg = ft.AlertDialog(
            title=ft.Row([
                ft.Icon("warning_rounded", color=ft.colors.ORANGE_ACCENT,
                        size=32),
                ft.Text("GSHEET URL EXISTS", weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER, size=20)
            ], spacing=10),
            content=ft.Text(f"This URL is for {data['owner'].upper()}"
                            f" that is added on {data['month']} "
                            f"{data['year']}.\nWould you like to view the "
                            f"saved GSheet URL?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda a: a.page.close(dlg)),
                ft.ElevatedButton("Proceed", on_click=proceed_event,
                                  bgcolor=ft.colors.BLUE_ACCENT,
                                  color=ft.colors.WHITE)
            ],
            modal=True, bgcolor=ft.colors.GREY_900)

        gsheet_url.current.value = ""
        e.page.open(dlg)
        e.page.update()
        return

    # Trigger first the recently added event to load recents list
    gsheetlister_control.show_recently_added()

    # Then proceed adding and creating the gsheet URL
    if url:
        # Create a GSheetURL control and append it to the gsheets cont
        gsheeturl_control = GSheetURL(url)
        gsheet_url.current.value = ""
        gsheetlister_control.append(gsheeturl_control, first=True)
        gsheetlister_control.disable_filter_controls(True)
        add_url_button.current.disabled = True
        download_button.current.disabled = True
        progressbar_control.reset()
        e.page.update()

        def fetch_completed(**kwargs):
            """ Callback method after the data fetch has been completed. """
            DATA[kwargs["owner"]] = kwargs["final_data"]
            gsheeturl_control.update_display_labels(
                owner=kwargs["owner"], month=kwargs["month"],
                timestamp=kwargs["timestamp"], diskload=False)
            # Update the states of UI Controls
            add_url_button.current.disabled = False
            download_button.current.disabled = False
            gsheetlister_control.disable_filter_controls(False)
            e.page.update()

            # Save the downloaded data to its own JSON file
            data_dir = Path(Reader.BASE_PATH / "downloads/data")
            data_dir.mkdir(parents=True, exist_ok=True)
            owner_formatted = kwargs["owner"].lower().replace(" ", "-")
            filename = f"{kwargs["month_num"]}-{owner_formatted}.json"
            file = data_dir / filename
            with open(file, "w") as outfile:
                json.dump(kwargs, outfile)

            # Save to the gsheetlister RECENTS list
            gsheetlister_control.add_recents(filename)
            # Save to the gsheetlister URLS_DB dictionary
            month, year = kwargs["month"].split()
            month_num = kwargs["month_num"].split("-")[0]
            gsheetlister_control.add_urlsdb(url=kwargs["url"],
                                            month=month, year=year,
                                            month_num=month_num,
                                            owner=kwargs["owner"])

        def progress_callback(**kwargs):
            """ Callback for the progress bar control to update. """
            progressbar_control.update_progress(**kwargs)

        # Create a Reader class to fetch data and pass the required callbacks
        reader = Reader(url=url)
        reader.fetch_data(sheet_identifier="*-",
                          progress=progress_callback,
                          completed=fetch_completed)


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

    # Google Sheet Adder Card
    hint = "https://docs.google.com/spreadsheets/..."
    sheet_url_card = ft.Card(content=ft.Container(
        content=ft.Row([
            ft.TextField(ref=gsheet_url,
                         label="Google Sheet URL:",
                         border_color=ft.colors.GREY_500,
                         hint_text=hint,
                         expand=4),
            ft.ElevatedButton(ref=add_url_button,
                              text="ADD URL",
                              icon="add_link_sharp", height=50,
                              expand=1,
                              style=Styles.add_url_style,
                              on_click=add_url_button_event),
            ft.OutlinedButton(content=ft.Icon("settings_rounded",
                              size=30, color=ft.colors.WHITE60),
                              width=55, height=50,
                              style=Styles.settings_style,
                              tooltip="DATA SETTINGS ")
        ], spacing=15), padding=20))

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
    page.add(sheet_url_card)
    page.add(gsheetlister_control)
    page.add(download_progress_container)


# Run the main Flet Window App
ft.app(main)
