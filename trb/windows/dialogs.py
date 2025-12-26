import wx
from os.path import isdir
from os import getcwd

def error_dialog(message, caption="Error", parent=None):
    """
    Displays a simple error message dialog.
    """
    dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_ERROR)
    dlg.ShowModal()  # Shows the dialog modally (blocks until closed)
    dlg.Destroy()

def warning_dialog(message, caption="Error", parent=None):
    """
    Displays a simple error message dialog.
    """
    dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_EXCLAMATION)
    dlg.ShowModal()  # Shows the dialog modally (blocks until closed)
    dlg.Destroy()

def file_browse_dialog(parent, def_start_dir: str, wildcard, title="Choose a file:", rel_dir=""):

    ctrl_text = ""
    if isdir(def_start_dir):
        start_path = def_start_dir
    else:
        start_path = getcwd()

    with wx.FileDialog(parent, title, defaultDir=start_path, wildcard=wildcard,
                      style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dirDialog:
        if dirDialog.ShowModal() == wx.ID_OK:
            selected_path = dirDialog.GetPath()
            return selected_path

    return None

def dir_browse_dialog(parent, def_start_dir: str, text_ctl: wx.TextCtrl = None, title="Choose a directory:",
                      rel_dir=""):

    ctrl_text = ""
    if text_ctl is not None:
        ctrl_text = text_ctl.GetValue()
        if ctrl_text == ".":
            ctrl_text = rel_dir
        else:
            ctrl_text = rel_dir + ctrl_text
    if isdir(ctrl_text):
        start_path = ctrl_text
    elif isdir(def_start_dir):
        start_path = def_start_dir
    else:
        start_path = getcwd()

    with wx.DirDialog(parent, title,
                      defaultPath=start_path,
                      style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON) as dirDialog:
        if dirDialog.ShowModal() == wx.ID_OK:
            selected_path = dirDialog.GetPath()
            if text_ctl is not None:
                text_ctl.SetValue(selected_path)
            return selected_path

    return None

    # def error_dialog(parent, message, caption="Error"):
    #     """
    #     Displays a simple error message dialog.
    #     """
    #     dlg = MessageDialog(parent, message, caption, wx.OK | wx.ICON_ERROR)
    #     dlg.ShowModal()  # Shows the dialog modally (blocks until closed)
    #     dlg.Destroy()