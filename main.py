import wx
import wx.lib.newevent
from trb.MainWindow import MainWindow #, wxLogEvent, EVT_WX_LOG_EVENT
from trb.settings import Settings
from trb.loggers import WindowLogger, EVT_WX_LOG_EVENT, log_init


class TVRenameWindow(wx.App):
    def OnInit(self):
        logger = log_init()
        self.settings = Settings()
        self.settings.load()
        # logger.setLevel(Settings.log_level)
        # self.settings.save()
        self.frame = MainWindow(self.settings, None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()

        logger.addHandler(WindowLogger(self.frame.log_box))
        self.Bind(EVT_WX_LOG_EVENT, self.frame.onLogEvent)

        return True


if __name__ == "__main__":
    TVRenameBuddy = TVRenameWindow(0)
    TVRenameBuddy.MainLoop()
