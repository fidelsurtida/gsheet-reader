import flet as ft
from controls.gsheeturl import GSheetURL
from modules.reader import Reader
import modules.reader as tempreader


def set_window_properties(page: ft.Page):
    page.title = "GSheet Reader"
    page.window.width = 900
    page.window.height = 600
    page.window.resizable = False
    page.window.always_on_top = True
    page.theme_mode = ft.ThemeMode.DARK


# CONTROL STYLES
add_url_style = ft.ButtonStyle(
    shape=ft.RoundedRectangleBorder(radius=8),
    overlay_color={
        ft.ControlState.PRESSED: ft.colors.GREEN_900
    },
    color={
        ft.ControlState.DEFAULT: ft.colors.GREEN_900,
        ft.ControlState.HOVERED: ft.colors.GREEN_100,
    },
    bgcolor={
        ft.ControlState.HOVERED: ft.colors.GREEN_300,
        ft.ControlState.DEFAULT: ft.colors.GREEN_500,
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
    },
    bgcolor={
        ft.ControlState.HOVERED: ft.colors.BLUE_400,
        ft.ControlState.DEFAULT: ft.colors.BLUE_500,
    }
)


# --------------------------------
# FLET MAIN FUNCTION ENTRY POINT
# --------------------------------
def main(page: ft.Page):
    # Set the Window Properties
    set_window_properties(page)

    # Flet Control References
    gsheet_url = ft.Ref[ft.TextField]()
    download_button = ft.Ref[ft.CupertinoButton]()
    add_url_button = ft.Ref[ft.FilledButton]()
    progress_container = ft.Ref[ft.Column]()
    progress_bar = ft.Ref[ft.ProgressBar]()
    gsheets_url_column = ft.Ref[ft.Column]()

    # On-Click Button event of generate CSV button
    def download_button_event(e):
        url = gsheet_url.current.value
        if url:
            download_button.current.disabled = True
            progress_container.current.visible = True
            page.update()
            # tempreader.generate_csv_report(url, download_button, page)
        else:
            print("INVALID GSHEET URL...")

    def add_url_button_event(e):
        """
        This button event will add a GSheetURL control to the container
        UI interface and perform a data fetch on the Google Sheet.
        """
        url = gsheet_url.current.value
        if url:
            # Create a GSheetURL control and append it to the gsheets cont
            gsheeturl_item = GSheetURL(url)
            gsheet_url.current.value = ""
            gsheets_url_column.current.controls.append(gsheeturl_item)
            page.update()

            # Create a Reader based from the passed url and specify a completed
            # callback method to update certain UI controls
            def fetch_completed(params):
                gsheeturl_item.update_display_labels(owner=params["owner"])

            reader = Reader(url=url)
            reader.fetch_data(sheet_identifier="*-", completed=fetch_completed)

    # Google Sheet Adder Card
    hint = "https://docs.google.com/spreadsheets/..."
    sheet_url_card = ft.Card(content=ft.Container(
        content=ft.Row([
            ft.TextField(ref=gsheet_url,
                         label="Google Sheet URL:",
                         border_color=ft.colors.GREY_500,
                         hint_text=hint,
                         expand=4),
            ft.FilledButton(ref=add_url_button,
                            text="ADD URL",
                            icon="add_link_sharp", height=50,
                            expand=1,
                            style=add_url_style,
                            on_click=add_url_button_event)
        ], spacing=20), padding=20))

    # Google Sheets List Container
    sheet_list_container = ft.Card(content=ft.Column([
        ft.Container(content=ft.Row([
                        ft.Icon("event_note_rounded",
                                color=ft.colors.WHITE60),
                        ft.Text("GSHEETS SAVED URLS",
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE54)
                     ]),
                     bgcolor=ft.colors.BLUE_GREY_900,
                     padding=ft.padding.only(20, 8, 20, 10),
                     border_radius=ft.border_radius.only(12, 12, 0, 0)),

        ft.Container(content=ft.Column([],
                     ref=gsheets_url_column, spacing=15,
                     scroll=ft.ScrollMode.AUTO, height=250),
                     padding=ft.padding.all(10),
                     margin=ft.margin.only(5, 0, 5, 0),
                     border_radius=5)
    ]), height=350)

    # Download Button and Progress Bar Container
    download_progress_container = ft.Container(content=ft.Row([
        ft.Column([
            ft.Text("Downloading Sheets..."),
            ft.ProgressBar(ref=progress_bar, bar_height=8,
                           border_radius=ft.border_radius.all(5),
                           color=ft.colors.GREEN_400,
                           value=0.6)
        ], ref=progress_container, expand=5),

        ft.FilledButton(
            ref=download_button,
            text="DOWNLOAD DATA",
            icon="cloud_download_sharp",
            on_click=download_button_event,
            expand=2, height=50,
            style=download_data_style)
    ], spacing=30), height=70, padding=10)

    # Add the main elements of the application
    page.add(sheet_url_card)
    page.add(sheet_list_container)
    page.add(download_progress_container)


# Run the main Flet Window App
ft.app(main)
