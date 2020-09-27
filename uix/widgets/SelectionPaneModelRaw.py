from uix.widgets.SelectionPane import *

"""
Architecture selection
"""


class SelectionPaneModelRaw(SelectionPane):
    def __init__(self):
        super(SelectionPaneModelRaw, self).__init__(
            x=big_window_haut // 2 + int(0.75 * menu_button_w),
            y=2 * big_window_haut // 3,
            title="Model's Design ?",
            folder=models_path,
            extension=".net")
