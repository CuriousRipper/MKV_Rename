import logging
from os import listdir
import json
from trb.util import lower_key, strip_field_name
import re

class DB_DiskManager:
    def __init__(self, release_path):
        self.release_path = release_path
        self.disks = DB_DiskManager.load_disks(release_path)


    @staticmethod
    def load_disks(release_path):
        disks = {}
        for file in listdir(release_path):
            match = re.search(r"(?<=dis[ck])\d+(?=-summary)", file)
            if match:
                idx = match.group(0)
                disks[idx] = DB_Disk(release_path + "/disc" + idx)


        return disks


class DB_Disk:
    def __init__(self, base_name: str):
        self.titles = None
        self.base_name = base_name
        self.slug, self.name, self.format, self.display = self.load_json()
        self.load_titles()

        self.compare()

        # self.year = json.get('year', 'Unknown')
        # self.UPC = json.get('upc', 'Unknown')
        # self.ASIN = json.get('asin', 'Unknown')
        # self.locale = json.get('locale', 'Unknown')
        # self.release_date = json.get('year', 'Unknown')
        # self.slug = json.get('year', 'Unknown')
        # self.title = json.get('year', 'Unknown')


    def load_titles(self):
        summary_file = self.base_name + "-summary.txt"
        try:
            with open(summary_file) as fptr:
                self.titles = DB_Disk._parse_titles(fptr.readlines())
        except Exception as e:
            logging.error("Encountered error parsing: " + summary_file + "\t" + str(e))

    def get_title(self, src: str):
        for title in self.titles:
            if title["src"] == src:
                return title

    @staticmethod
    def _parse_line(lower, title, line):
        keys = {
            "source": "src",
            "type": "type",
            "name": "name",
            "season": "season",
            "episode": "episode",
            "file name": "rec_name",
            "filename": "rec_name",
            "description": "desc"
        }
        # print(line)
        for key, new_key in keys.items():
            # print("\t" + key)
            if lower.startswith(key):
                title[new_key] = strip_field_name(line)
                # print("\t\t" + str(title))
                return
        # print("\tNo keys match line")

    @staticmethod
    def _parse_titles( lines: list[str]):
        titles = []
        title = {}
        for line in lines:
            lower = line.lower()
            if lower.startswith("name:"):
                if len(title) > 0:
                    # print(title)
                    titles.append(title)
                title = {"name": strip_field_name(line)}
            else:
                DB_Disk._parse_line(lower, title, line)
            # elif lower.startswith("type:"):
            #     type_name = line[6:].strip()
            #     # if type_name == "DeletedScene" or type_name == "Extra":
            #     if type_name == "Extra":
            #         title['type'] = "extra"
            # elif lower.startswith("file name:"):
            #     title['filename'] = line
            # elif lower.startswith("source file name:"):
            #     title['filename'] = line


        if len(title) > 0:
            titles.append(title)

        # print(discs)
        return titles

    def load_json(self):
        json_file = self.base_name + ".json"
        # try:
        if True:
            with open(json_file) as fptr:
                parsed =  lower_key(json.load(fptr))
                slug = parsed.get('slug', '')
                name = parsed.get('name', '')
                format = parsed.get('format', '')
                display = name + " - " + format + " - " + slug
                if not slug:
                    slug = "None"
                if not name:
                    name = "Unknown"
                if not format:
                    format = "Unknown Format"

                return slug, name, format, display

        # except Exception as e:
        #     logging.error("Encountered error parsing: " + json_file + "\t" + str(e))

        return "", "", "", ""

    def compare(self):
        """
        Perform comparison of title data in json file and summary file if present.
        Issue warnings if they do not match
        :return: None
        """
        pass
