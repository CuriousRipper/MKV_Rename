import logging
import re

def parse_makemkv_log(filename: str):

    lines = []
    with open(filename) as fptr:
        lines = fptr.readlines()

    src_files = []
    disks = []
    for line in lines:
        if -1 != line.find("was added as title"):
            # line = line.strip()
            match = re.search(r"(?<=File ).*(?= was)", line)
            if not match:
                logging.warning("No filename detected in: " + line.strip())
                break

            # clear titles on new disk scan
            if re.search(r"#0$", line):
                src_files = []

            src_files.append(match.group(0))

        if re.search(r"Saving \d* titles into directory file", line):
            path = re.search(r"(?<=file:).*$", line).group(0).strip()
            title = path[path.rfind("/") + 1:]

            # trim leading slashes on windows (//C:/)
            lead_slash = re.search(r"/*[a-zA-zZ]:", path)
            if lead_slash:
                trim_length = len(lead_slash.group(0)) - 2
                path = path[trim_length:]

            disk = {
                "title": title,
                "path": path,
                "src_files": src_files
            }
            disks.append(disk)
            src_files = []

    # print(disks)
    return disks

