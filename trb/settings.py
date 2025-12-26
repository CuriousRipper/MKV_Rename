import json
from os.path import exists
from trb.windows.SettingsDialog import SettingsDialog
from trb.windows.dialogs import error_dialog
from wx import ID_ANY, ID_OK
class Settings:
    def __init__(self):
        self.disk_db_path = 'C:/cygwin64/home/james/projects/diskdb/data/data/data/'
        self.default_video_input = "C:/Video"
        self.default_video_output = "./"
        self.default_makemkv_log_folder = "C:/Video"

        self.update_default_video_input = False
        self.update_default_video_output = False
        self.update_default_makemkv_log_folder = False

    def load(self, filename="settings.json"):
        if not exists(filename):
            self.show_dialog()
        with open(filename) as fptr:
            settings = json.load(fptr)
            keys = settings.keys()
            if "default_video_output" in keys:
                self.default_video_output = settings["default_video_output"]

        if "default_video_input" in keys:
            self.default_video_output = settings["default_video_output"]

    def show_dialog(self):
        with SettingsDialog(None, ID_ANY, "") as sd:
            if sd.ShowModal() == ID_OK:
                path = sd.discDB_datafolder.GetValue()
                if not exists(path):
                    error_dialog("DiscDB data folder dose not exist. Exiting!")
                    exit(1)

                series_path = path + "/series"
                movie_path = path + "/movie"
                if (not exists(series_path)) or (not exists(movie_path)):
                    error_dialog("DiscDB data folder does not appear valid. Exiting!")
                    exit(1)
                self.disk_db_path = path
                self.save()
                return
        error_dialog("No DiscDB data folder set. Exiting!")
        exit(1)

    def save(self, filename="settings.json"):
        try:
            with open(filename, 'w') as fptr:
                json.dump(self.__dict__, fptr, indent=True)
        except:
            print("Could not save settings")

