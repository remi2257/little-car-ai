from uix.my_gui.widgets import SelectionPane

from src.const import big_window_haut, menu_button_w, trained_model_path

"""
Trained model selection
"""


class SelectionPaneModelTrain(SelectionPane):
    def __init__(self):
        super(SelectionPaneModelTrain, self).__init__(
            x=big_window_haut // 2 + int(0.75 * menu_button_w),
            y=big_window_haut // 3,
            title="Trained Model ?",
            folder=trained_model_path,
            extension=".h5")

        self.add_item("None")

    def get_chosen_item_path(self):
        if self._items[self._chosen_id] == "None":
            return None
        return super(SelectionPaneModelTrain, self).get_chosen_item_path()
