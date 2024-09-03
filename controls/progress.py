# ---------------------------------------------------
# progress.py - Progress Class
# ---------------------------------------------------
# A class that represents a flet custom control for
# displaying a progressbar with accompanied text
# used in showing status messages. This also has
# methods to easily change the progress value and
# status messages.
# ---------------------------------------------------

import flet as ft


class Progress(ft.Column):

    def __init__(self):
        """
        Custom Flet Control for displaying a progress bar with status text
        message. Contains methods to easily change value, message and reset
        the status of the control.
        """
        super().__init__()

        # Declaration of flet control references
        self._message_text_left = ft.Ref[ft.Text]()
        self._message_text_right = ft.Ref[ft.Text]()
        self._message_text_center = ft.Ref[ft.Text]()
        self._center_icon = ft.Ref[ft.Icon]()
        self._center_container = ft.Ref[ft.Container]()
        self._progress_bar = ft.Ref[ft.ProgressBar]()

        # Column Parameters
        self.expand = 5

        # Initialize the custom controls Design of progress bar
        self.controls = [
            ft.Row([
                ft.Text("", ref=self._message_text_left),
                ft.Container(content=ft.Row([
                    ft.Icon("account_circle", ref=self._center_icon,
                            size=16, color=ft.colors.WHITE),
                    ft.Text("FIDEL JESUS SURTIDA", size=12,
                            weight=ft.FontWeight.BOLD,
                            ref=self._message_text_center)
                    ], spacing=3),
                    ref=self._center_container,
                    bgcolor=ft.colors.BLUE_800, border_radius=10,
                    padding=ft.padding.symmetric(4, 7), visible=False),
                ft.Text("", ref=self._message_text_right)
            ], spacing=5),
            ft.ProgressBar(ref=self._progress_bar, bar_height=8,
                           border_radius=ft.border_radius.all(5),
                           color=ft.colors.GREEN_400,
                           value=0)
        ]

    def update_progress(self, *, left="", center="", right="", value=0):
        """ Updates the message and progress value of this control. """
        self._message_text_left.current.value = left
        self._message_text_right.current.value = right
        self._center_container.current.visible = False
        if center:
            self._center_container.current.visible = True
            self._message_text_center.current.value = center.upper()
        self._progress_bar.current.value = value

        # Change to red style when detected "Download Failed" text on left
        if left == "Download Failed":
            self._message_text_left.current.color = ft.colors.RED_ACCENT
            self._message_text_right.current.color = ft.colors.RED_ACCENT
            self._center_container.current.bgcolor = ft.colors.RED_ACCENT_700
            self._progress_bar.current.color = ft.colors.RED_ACCENT

        # Change the appearance of the message if progress bar is finished
        if value == 1:
            self._message_text_left.current.color = ft.colors.GREEN_400
            self._message_text_right.current.color = ft.colors.GREEN_400
            self._center_container.current.bgcolor = ft.colors.GREEN_700
            self._center_icon.current.name = "cloud_done_rounded"

        self.update()

    def reset(self):
        """ Resets the progress bar to show no message and 0 value. """
        self._message_text_left.current.value = ""
        self._message_text_center.current.value = ""
        self._message_text_right.current.value = ""
        self._center_container.current.visible = False
        self._center_icon.current.name = "account_circle"
        self._center_container.current.bgcolor = ft.colors.BLUE_800
        self._message_text_left.current.color = ft.colors.WHITE
        self._message_text_right.current.color = ft.colors.WHITE
        self._progress_bar.current.color = ft.colors.GREEN_400
        self._progress_bar.current.value = 0
        self.update()
