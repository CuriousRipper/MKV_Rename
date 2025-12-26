import logging
import os
import re

from trb.TVTableManager import TVTableManager
from trb.glade.TVFrameBase import TVFrameBase
from trb.settings import Settings

from trb.parsers.db_indexer import build_index, asin_search, upc_search
from trb.parsers.db_disk_manager import DB_DiskManager, DB_Disk
from trb.parsers.makemkv_log_parser import parse_makemkv_log

from trb.windows.dialogs import dir_browse_dialog, file_browse_dialog
from pathlib import Path

from trb.util import files_present


class MainWindow(TVFrameBase):
    def __init__(self, settings: Settings, *args, **kwds):
        TVFrameBase.__init__(self, *args, **kwds)
        self.tv_table_manager: TVTableManager = None
        self.settings = settings
        self.populate_defaults()

        # TV Table Manager
        self.tv_table_manager = TVTableManager(self.episode_grid)
        self.tv_table_manager.clear_table()


        # Intermediate Parameters
        self.makemkv_log_disks = []
        self.log_file = None
        self.db_disks = None
        self.release_path = ""

        # Final Parameters
        self.selected_makemkv_disk = None
        self.selected_discDB_disk:DB_Disk = None
        self.selected_video_dir = ""


    def onLogEvent(self, event):
        """
        Add event.message to text window
        :param event:
        :return: None
        """
        msg = event.message.strip("\r") + "\n"
        self.log_box.AppendText(msg)
        event.Skip()

    def populate_defaults(self):
        self.video_input_field.SetValue( self.settings.default_video_input )
        self.video_output_field.SetValue( self.settings.default_video_output )

    def populate_table(self):
        if (not self.selected_video_dir or
                not self.selected_discDB_disk or
                not self.selected_makemkv_disk):
            self.episode_grid.Disable()
            return

        self.episode_grid.Enable()
        # if not self.tv_table_manager:
        #     self.tv_table_manager = TVTableManager(self.episode_grid)
        #     # self.tv_table_manager.init_frame()

        # print(self.release_path)
        video_dir = self.selected_video_dir
        log_disk = self.selected_makemkv_disk
        db_disk = self.selected_discDB_disk
        self.tv_table_manager.initial_populate(video_dir, log_disk, db_disk)

    def browse_input(self, event):  # wxGlade: TVFrameBase.<event_handler>
        path = self.settings.default_video_input
        title = "Where are your videos?"
        dir_browse_dialog(self, path , self.video_input_field, title)
        self.video_input_enter()
        event.Skip()

    def browse_output(self, event):  # wxGlade: TVFrameBase.<event_handler>
        if self.settings.default_video_output == "." or self.settings.default_video_output == "./":
            path = self.settings.default_video_input
        else:
            path = self.settings.default_video_output
        title = "Where should the renamed files go?"
        dir_browse_dialog(self, path , self.video_output_field, title)
        event.Skip()

    def search_series(self, event):  # wxGlade: TVFrameBase.<event_handler>
        search_term = self.search_txt_ctrl.GetValue()
        db_path = self.settings.disk_db_path + "/series"

        if self.asin_radio.GetValue():
            self.release_path = asin_search(search_term, "indices/series.json", db_path)

        elif self.upc_radio.GetValue():
            self.release_path = upc_search(search_term, "indices/series.json", db_path)

        else:
            self.release_path = ""

        self._new_release()

        event.Skip()

    def browse_db(self, event):  # wxGlade: TVFrameBase.<event_handler>
        title = "Select the release folder:"
        db_path = self.settings.disk_db_path
        full_release_path: str = dir_browse_dialog(self, db_path, None, title)
        if os.path.exists(full_release_path):
            full_release_path = full_release_path.replace("\\", "/")
            tail = re.search(r"(?<=/data/series/).*/.*", full_release_path)
            if tail:
                self.release_path = tail.group(0)
                self._new_release()
        event.Skip()

    def browse_log(self, event):  # wxGlade: TVFrameBase.<event_handler>
        wildcard = "Log Files (*.log)|*.log|All Files (*.*)|*.*"
        log = file_browse_dialog(self, self.settings.default_makemkv_log_folder, wildcard,"MakeMKV Log File")
        if log:
            if self.settings.update_default_makemkv_log_folder:
                self.settings.default_makemkv_log_folder = Path(log)
            self.log_file = log
            self.makemkv_log_disks = parse_makemkv_log(log)

        self.populate_log_select()
        event.Skip()

    def copy_filenames(self, event):  # wxGlade: TVFrameBase.<event_handler>
        self.tv_table_manager.copy_db_name()
        event.Skip()

    def generate_filenames(self, event):  # wxGlade: TVFrameBase.<event_handler>
        print("Event handler 'generate_filenames' not implemented!")
        event.Skip()

    def do_rename(self, event):  # wxGlade: TVFrameBase.<event_handler>
        rename_log = logging.getLogger("rename")
        src_path = self.video_input_field.GetValue()
        dest_path = self.video_output_field.GetValue()

        if dest_path.startswith("."):
            dest_path = src_path + "/" + dest_path

        for row in range(self.episode_grid.GetNumberRows()):
            src = self.episode_grid.GetCellValue(row, 3).strip()
            original_name = self.episode_grid.GetCellValue(row, 4).strip()
            new_name = self.episode_grid.GetCellValue(row,5).strip()

            if not new_name:
                logging.warning(f"Cannot rename {original_name} the rename to field is blank!")
                continue

            original_full = src_path + "/" + original_name
            new_full = dest_path + "/" + new_name

            logging.info(f'Renaming "{original_full}" to "{new_full}" based on source "{src}"')
            rename_log.info(f"{src}\t{original_full}\t{new_full}")
            os.rename(original_full, new_full)

        event.Skip()

    def update_summary(self, event):  # wxGlade: TVFrameBase.<event_handler>
        logging.info("Event handler 'update_summary' not implemented!")
        event.Skip()

    def save_status(self, event):  # wxGlade: TVFrameBase.<event_handler>
        print("Event handler 'save_status' not implemented!")
        event.Skip()

    def load_status(self, event):  # wxGlade: TVFrameBase.<event_handler>
        print("Event handler 'load_status' not implemented!")
        event.Skip()

    def build_index(self, event):  # wxGlade: TVFrameBase.<event_handler>
        build_index("indices/series.json", self.settings.disk_db_path + "/series")
        event.Skip()

    def populate_disk_select(self):
        full_path = self.settings.disk_db_path + "/series/" + self.release_path
        self.db_disks = DB_DiskManager(full_path)

        self.discDB_disk_combo.Clear()
        for disk_idx in self.db_disks.disks:
            disk = self.db_disks.disks[disk_idx]
            self.discDB_disk_combo.Append(disk.display, disk_idx)
            # print(disk)

        self.discDB_disk_combo.Enable()

    def populate_log_select(self):
        self.makemkv_disk_combo.Clear()
        for disk in self.makemkv_log_disks:
            text = disk['title'] + " - " + disk['path']
            self.makemkv_disk_combo.Append(text)

        self.makemkv_disk_combo.Enable()

    def makemkv_disk_selected(self, event):
        idx = self.makemkv_disk_combo.GetSelection()
        self.selected_makemkv_disk = self.makemkv_log_disks[idx]
        self.video_input_field.SetValue(self.selected_makemkv_disk['path'])
        print(self.selected_makemkv_disk)
        self.video_input_enter()
        event.Skip()

    def video_input_enter(self, event=None):
        input_dir = self.video_input_field.GetValue()

        if not files_present(input_dir, "mkv"):
            return

        self.selected_video_dir = input_dir
        self.populate_table()
        if event:
            event.Skip()

    def discDB_disk_selected(self, event):
        idx =  self.discDB_disk_combo.GetSelection()
        idx_str = self.discDB_disk_combo.GetClientObject(idx)
        self.selected_discDB_disk = self.db_disks.disks[idx_str]
        self.populate_table()
        event.Skip()

    def _new_release(self):
        self.tv_table_manager.clear_table()
        if self.release_path:
            self.populate_disk_select()
        else:
            self.discDB_disk_combo.Disable()
