import flet as ft
import modules.reader as reader


def set_window_properties(page: ft.Page):
    page.title = "GSheet Reader"
    page.window.width = 500
    page.window.height = 300
    page.window.resizable = False
    page.window.always_on_top = True
    page.theme_mode = ft.ThemeMode.DARK


def main(page: ft.Page):
    # Set the Window Properties
    set_window_properties(page)

    # Variable References
    hint = "https://docs.google.com/spreadsheets..."
    url_textfield = ft.Ref[ft.TextField]()
    download_button = ft.Ref[ft.CupertinoButton]()

    # On-Click Button event of generate CSV button
    def download_button_event(e):
        url = url_textfield.current.value
        if url:
            download_button.current.disabled = True
            page.update()
            reader.generate_csv_report(url, download_button, page)
        else:
            print("INVALID GSHEET URL...")

    url_card_container = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.TextField(ref=url_textfield,
                                 label="Gsheet URL:",
                                 border_color=ft.colors.GREY_500,
                                 hint_text=hint),
                    ft.Row([
                        ft.CupertinoButton(
                            ref=download_button,
                            content=ft.Text("Download CSV Data",
                                            weight=ft.FontWeight.BOLD),
                            opacity_on_click=0.5,
                            color=ft.colors.WHITE60,
                            bgcolor=ft.colors.BLUE_600,
                            disabled_color=ft.colors.GREY_700,
                            on_click=download_button_event,
                        )
                    ], alignment=ft.MainAxisAlignment.END)
                ], spacing=20
            ), padding=20,
        ), height=180
    )

    page.add(url_card_container)


ft.app(main)
