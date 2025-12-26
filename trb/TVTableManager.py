import wx.grid
import logging
from trb.util import filtered_ls, get_title_number
from trb.parsers.db_disk_manager import DB_Disk
class TVTableManager:
    def __init__(self, grid: wx.grid):
        self.mkv_files = None
        self.db_disk:DB_Disk = None
        self.log_disk = {}

        self.episode_grid = grid # self.episode_grid.CreateGrid(1, 12)  # 1 rows, 12 columns
        self.griddata = []

    def initial_populate(self, video_dir: str, log_disk: dict, selected_discDB_disk: DB_Disk) -> None:
        self.mkv_files = filtered_ls(video_dir, "mkv")
        self.log_disk = log_disk
        self.db_disk = selected_discDB_disk
        pairings = self._pair_titles()

        grid: wx.grid = self.episode_grid
        self.clear_table(False)
        grid.BeginBatch()
        self.episode_grid.AppendRows(len(pairings))
        for row, pairing in enumerate(pairings):
            for col, value in enumerate(["1", "Cpy", "Gen", pairing[0], pairing[1]]):
                grid.SetCellValue(row, col, value)
                # print(str(row) + ":" + str(col) + ":\t" + value)


        widths = [40, 40, 40, 105, 250, 250, 70, 125, 45, 45, 180, 225, 180, 750]
        for col, width in enumerate(widths):
            grid.SetColSize(col, width)
        grid.EndBatch()

        self._load_db_parameters()
        grid.ForceRefresh()


        # self.episode_grid
    def clear_table(self, refresh=True):
        grid = self.episode_grid
        row_count = self.episode_grid.GetNumberRows()
        if row_count:
            self.episode_grid.DeleteRows(0, row_count)
        if refresh:
            grid.ForceRefresh()

    def _pair_titles(self):
        rows = []
        src_files = self.log_disk['src_files']
        for file in self.mkv_files:
            title_num = get_title_number(file)
            if title_num != -1 and title_num < len(src_files):
                rows.append((src_files[title_num], file))
            else:
                rows.append(("", file))

        return rows

    def _load_db_parameters(self) -> None:

        grid = self.episode_grid
        grid.BeginBatch()
        col_keys = {
            7: 'type',
            6: 'season',
            10: 'name',
            8: 'episode',
            13: 'desc',
            11: 'rec_name'
        }
        for row in range(self.episode_grid.GetNumberRows()):
            title = self.db_disk.get_title(grid.GetCellValue(row, 3))
            for col, key in col_keys.items():
                if key in title.keys():
                    grid.SetCellValue(row, col, title[key])


        grid.EndBatch()
        grid.ForceRefresh()


    def copy_db_name(self):
        if not self.db_disk:
            logging.warning("No database disk loaded")
            return
        for row in range(self.episode_grid.GetNumberRows()):
            self.copy_db_row(row)

    def copy_db_row(self, row):
        self.episode_grid.SetCellValue(row, 5, self.episode_grid.GetCellValue(row,11))

    # def init_frame(self):
    #     #
    #
    #     self.episode_grid.SetColLabelValue(0, "Rename") # (checkbox)
    #     self.episode_grid.SetColLabelValue(1, "Cpy")  # copy button)
    #     self.episode_grid.SetColLabelValue(2, "Gen")  # generate button)
    #     self.episode_grid.SetColLabelValue(3, "Source")  # Source file, ro
    #     self.episode_grid.SetColLabelValue(4, "Current Name")  # text, ro
    #     self.episode_grid.SetColLabelValue(5, "Rename to:")  # text
    #     self.episode_grid.SetColLabelValue(6, "Type")  # Pull down
    #     self.episode_grid.SetColLabelValue(7, "Ep #")  #Number or range
    #     self.episode_grid.SetColLabelValue(8, "Sp #")  # Number or range
    #     self.episode_grid.SetColLabelValue(9, "Name")  # Text rw
    #     self.episode_grid.SetColLabelValue(10, "Custom Suffix")
    #     self.episode_grid.SetColLabelValue(11, "Summary File Description")
    #
    #     self.episode_grid.SetColFormatCustom(0, "bool")
    #     attr_checkbox = wx.grid.GridCellAttr()
    #     attr_checkbox.SetRenderer(wx.grid.GridCellBoolRenderer())
    #     attr_checkbox.SetEditor(wx.grid.GridCellBoolEditor())
    #     self.episode_grid.SetColAttr(0, attr_checkbox)
    #
    #     for col in [3, 4]:
    #         attr_readonly = wx.grid.GridCellAttr()
    #         attr_readonly.SetReadOnly(True)
    #         self.episode_grid.SetColAttr(col, attr_readonly)
    #
    #     attr_numeric = wx.grid.GridCellAttr()
    #     attr_numeric.SetEditor(wx.grid.GridCellNumberEditor())
    #     self.episode_grid.SetColAttr(8, attr_numeric)
    #
    #     attr_type = wx.grid.GridCellAttr()
    #     types = ["Episode", "Extra", "Deleted Scenes"]
    #     # attr_type = wxgrid.SetEditor
    #
    #
    #
    #
