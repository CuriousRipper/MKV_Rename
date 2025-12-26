# import wx
from os import write

import wx.lib.newevent
import logging

# create event type
wxLogEvent, EVT_WX_LOG_EVENT = wx.lib.newevent.NewEvent()

def log_init():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.basicConfig()
    file_handler = logging.FileHandler("DiskRenameBuddy.log")
    logger.addHandler(file_handler)
    rename = logging.getLogger("rename")
    rename.addHandler(logging.FileHandler("rename.log"))
    return logger

class WindowLogger(logging.Handler):
    """Custom handler to log messages to a Tkinter ScrolledText widget."""
    def __init__(self, text_ctl):
        super().__init__()
        self.log_panel = text_ctl
        # self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

    def emit(self, record):
        try:
            msg = self.format(record)
            evt = wxLogEvent(message=msg,levelname=record.levelname)
            wx.PostEvent(self.log_panel,evt)
        except (KeyboardInterrupt, SystemExit):
                raise
        except:
            self.handleError(record)
