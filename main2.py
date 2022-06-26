#! python3
# backupToZip.py
# Copies an entire folder and its contents into
# a zip file whose filename increments.

import zipfile, os
from pathlib import Path
from datetime import datetime
import re

FOLDER_TO_BACKUP = '/home/reecepbcups/Desktop/python-regex-backup-poc/test_backup'  # The directory to backup
BACKUP_DIRECTORY = '/home/reecepbcups/Desktop/python-regex-backup-poc/backups'  # The location to store the backups in
MAX_BACKUP_AMOUNT = 2  # The maximum amount of backups to have in BACKUP_DIRECTORY

STANDALONE_FILES_TO_BACKUP = [
    "/home/reecepbcups/imgs/pjn-m7lm_400x400.jpg",
    "/etc/python3.6/",
]

# Put in JSON File. Ability to have multiple folder to backup? (so we can grab other configs & files too)
# Or just add ability to specify absolute path to download other unique files
ignore = [
    "(P|p)aper.*jar",
    ".zip",
    "LuckPerms/dist"
]
regex = re.compile(r'|'.join(ignore))


# ------------
object_to_backup_path = Path(FOLDER_TO_BACKUP)
backup_directory_path = Path(BACKUP_DIRECTORY)
assert object_to_backup_path.exists()  # Validate the object we are about to backup exists before we continue
# Validate the backup directory exists and create if required
backup_directory_path.mkdir(parents=True, exist_ok=True)

# Get the amount of past backup zips in the backup directory already
existing_backups = [
    x for x in backup_directory_path.iterdir()
    if x.is_file() and x.suffix == '.zip' #and x.name.startswith('backup-')
]
# Enforce max backups and delete oldest if there will be too many after the new backup
oldest_to_newest_backup_by_name = list(sorted(existing_backups, key=lambda f: f.name))
while len(oldest_to_newest_backup_by_name) >= MAX_BACKUP_AMOUNT:  # >= because we will have another soon
    backup_to_delete = oldest_to_newest_backup_by_name.pop(0)
    backup_to_delete.unlink()


def backupToZip(debugFolders=True, debugFiles=True):
    # b-Jun_26_2022_04:53:55PM.zip
    zipFilename = f'b-{datetime.now().strftime("%b_%d_%Y_%I:%M:%S%p")}.zip'

    # Create the zip file.
    print('Creating %s...' % (zipFilename))
    backupZip = zipfile.ZipFile(os.path.join(BACKUP_DIRECTORY, zipFilename), 'w')

    # Walk the entire folder tree and compress the files in each folder.
    for foldername, subfolders, filenames in os.walk(FOLDER_TO_BACKUP):
        if debugFolders: print(f"\n-- FOLDER {foldername}")

        # add regex check here to ignore some files / folders if matching & print if ignored

        # Add the current folder to the ZIP file.
        # Could add folder exclusion regex here
        backupZip.write(foldername, compress_type=zipfile.ZIP_DEFLATED)

        # Add all the files in this folder to the ZIP file.
        for filename in filenames:

            # get the filename extension
            abs_file_path = os.path.join(foldername, filename)
            if regex.search(abs_file_path):
                # print(f"REGEX MATCH: {abs_file_path} ignoring.")
                continue
            else:
                # print the path
                if debugFiles: print('   ', abs_file_path)

            backupZip.write(os.path.join(foldername, filename), compress_type=zipfile.ZIP_DEFLATED)

    # Standalone file backups
    for filePath in STANDALONE_FILES_TO_BACKUP:
        # check if it is a file
        if os.path.isfile(filePath):
            print(f"Standalone: {filePath}")
            backupZip.write(filePath, compress_type=zipfile.ZIP_DEFLATED)
        elif os.path.isdir(filePath):
            print(f"Standalone dir: {filePath}")
            # loop through that dir
            for file in os.listdir(filePath):
                backupZip.write(os.path.join(filePath, file), compress_type=zipfile.ZIP_DEFLATED)
        else:
            print(f"Standalone: {filePath} is not a file or dir")
        
    backupZip.close()
    print('Done.')


backupToZip()