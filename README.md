MKV_Renamer is designed to rename videos made with MakeMKV using its logs and TheDiscDB. It currently only does Blu-ray 
disks of TV shows.  Eventually there will be a lot of support to make adding new shows less tedious.  

# Setup
## Setting up MakeMKV
1. View > Preferences > General > Miscellaneous  
Check "Log Debug Messages"
2. Restart (or close) MakeMKV
3. On windows, the log can be found in: ```C:\Users\<your username>\MakeMKV_log.txt```

 **Warning!! MakeMKV will overwrite the logs every time. It is a good idea to make a copy in a safe location every time you close it!!**


## Setting up MKV_Rename
### On Windows
1. Clone the DiscDB repo
2. Clone this repo
3. Run `setup.bat`  
   1. If python is not installed, it will try to install it from the Microsoft store. 
   2. If the store is disabled you may need to install it manually from [python.org](https://python.org/downloads)
   3. If you install python manually, you'll need to run the setup script again.
4. Run `run.bat`
5. Find your DiscDB repo and navigate to the inner data folder. It should be called data and have three folders inside it: series, movie, and sets.
6. (Optional) Close the program and edit additional options in the `settings.json` file. 

### On Linux
1. Clone the DiscDB repo
2. Clone this repo
3. Run `setup.sh`
   1.  It needs several prereqs. If you're using Debian/Ubuntu/Mint or another apt based distro it should be able to install them automatically, but I've only tested this on Ubuntu.
   2. If your using a distro without apt you'll need to install them manually, they are:
      1. python3 
      2. python3 virtual environment (python3-venv)
      3. python3 development (python3-dev)
      4. The GTK development libraries (libgtk-3-dev) 
4. Run `run.sh`
5. Find your DiscDB repo and navigate to the inner data folder. It should be called data and have three folders inside it: series, movie, and sets.
6. (Optional) Close the program and edit additional options in the `settings.json` file.# Workflow

# Workflow
1. Look for your series. You have a few options:
   1. You can use the UPC barcode on the packaging.
   2. You can look up the ASIN on amazon if you bought it from there.
   3. You can browse TheDiscDB folders to find the correct series and release.
2. From the pulldown menu in the `DiscDB disk` section (Left 2nd Row), select the appropriate disk.
3. In the `MakeMKV Log` section (to the right of step 2), select `Browse`, and find the MakeMKV log file.
4. Select the disk in the pull down menu to the right. 
5. The input folder should fill with the correct path. If it does not, select the path manually.
6. Verify the output path is where you want the files to go. It accepts absolute paths and paths relative to the input folder.
7. Click `Copy Filnames from DiscDB`.
8. If you don't like the recommend names you can edit them in the `Rename to:` column.
9. Click `Rename!`
