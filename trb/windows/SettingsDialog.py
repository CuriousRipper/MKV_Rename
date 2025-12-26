import logging

from trb.glade.SettingsDialogBase import SettingsDialogBase
from trb.windows.dialogs import dir_browse_dialog

class SettingsDialog(SettingsDialogBase):
    def browse_db_path(self, event):
        title = "Select the path for the DiscDB inner data folder. It should have series, movies, and sets in it."
        dir_browse_dialog(self, "" , self.discDB_datafolder, title)

        event.Skip()

    # def discDB_data_text(self, event):  # wxGlade: SettingsDialog.<event_handler>
    #     logging.info("Event handler 'discDB_data_text' not implemented!")
    #     self.discDB_datafolder.GetValue()
    #     event.Skip()
    #
    # def discDB_data_text_enter(self, event):  # wxGlade: SettingsDialog.<event_handler>
    #     logging.info("Event handler 'discDB_data_text_enter' not implemented!")
    #     event.Skip()

# end of class SettingsDialog
