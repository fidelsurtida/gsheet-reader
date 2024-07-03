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
        self._message_text = ft.Ref[ft.Text]()
        self._progress_bar = ft.Ref[ft.ProgressBar]()

        # Column Parameters
        self.expand = 5

        # Initialize the custom controls Design of progress bar
        self.controls = [
            ft.Text("", ref=self._message_text),
            ft.ProgressBar(ref=self._progress_bar, bar_height=8,
                           border_radius=ft.border_radius.all(5),
                           color=ft.colors.GREEN_400,
                           value=0)
        ]
