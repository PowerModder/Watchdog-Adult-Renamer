# Watchdog Adult Renamer
---------------------------------------------------------------------
This watchdog is able to monitor a given path and the subdirectories inside, scanning for adult media files and then match it with a site. Then it fetches back scene matching information and renames the media with the most-matched scene and according to user's preferences. Then it moves the matching scene to another location!
This application was made to be runned while you download files. However, you can try to match already existing files. See Known Issues for some notes to this.

### Features
  - Monitor a given path and the subdirectories for media files (videos).
  - Match site and scene with a supported site and fetch back the information.
  - Rename the media file with the most matched scene according to your preference and move it to new directory.
  - Dry-Run feature to actually test the functionality of the Watchdog.
  - Log the whole activity to a file for debugging purposes.
  - Script to create an exact clone of another directory.

### Changelog

[x] Initial support of some Adult sites (list of sites supported:sitelist.md)


### Usage and directions

1. Download the files as a zip and extract them to your desired location.
2. Open a terminal and run the command `pip install -r requirements.txt` or open the requirements.txt to see if you already satisfied the requirements.
3. Create an exact directory clone of your directory where you keep your already matched media files by running the CloneDir and by editing the following lines with your directories. This will be used as the DIRECTORY_TO_WATCH parameter.
```
source= ""
destination= ""
```
4. Open and edit the Watchdog.py preferences section
```
DIRECTORY_TO_WATCH = ""
DIRECTORY_TO_MOVE = ""
DIRECTORY_UNMATCHED = ""
pref_ID = False
pref_DryRun = True
```
5. Double click the Watchdog.py and if all done correct the Watchdog will be initiated.
6. Move or download files to the corresponding DIRECTORY_TO_WATCH/siteSubdirectory folder. This is important because the Watchdog uses the folder to match the site.

### Known issues
- Watchdog will report some times only created events for just moved files and not downloaded files. Go and comment out lines 82-84 and line 87 and uncomment line 86. This way your files will be processed for created or modified events. If a file creates both events then it will be processed two times. Couldn't debug it!
- Works great with media files that are downloaded from the source.

### To-Do - (Possible Features)
- Download posters from the original site, making folder and move the scene and the posters together. That way even if the PhoenixAdult Agent can't match the scene you can use the posters to Plex.
- Write the fetched information direct to the media file as metadata to avoid Phoenix Agent using embedded information

### Pull Requests, Recommendations or Questions
If you want to support a specific site, you can re-factor the code or you have a question please don't hesitate to make a pull request or open an issue. 
##### I will monitor this as my personal time allows me to do so.