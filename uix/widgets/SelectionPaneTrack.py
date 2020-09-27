from uix.widgets.SelectionPane import *

"""
Track selection
"""


class SelectionPaneTrack(SelectionPane):
    def __init__(self):
        super(SelectionPaneTrack, self).__init__(
            x=big_window_haut // 16,
            y=big_window_haut // 3,
            title="Choose ur Track",
            folder=track_files_path,
            extension=".tra")
