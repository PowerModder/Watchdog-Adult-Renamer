## Dependencies
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import re
import time
import logging
## Phoenix adult agent files
import PAsearchSites
## Other .py files
import LoggerFunction
import renamer_network1service
import renamer_sitebangbros

###################################################################### PREFERENCES ##################################################################################################
## Replace the following directories with yours. Use double \\
DIRECTORY_TO_WATCH = ""
DIRECTORY_TO_MOVE = ""
DIRECTORY_UNMATCHED = ""
## You prefer ID to your filename (True) or scene title (False)
pref_ID = False
## Change to (True) if you don't want the Watcher to actually move and rename the files (check matching result)
pref_DryRun = True
###################################################################### PREFERENCES ##################################################################################################
## Basic Logger information
loggerwatchdog = LoggerFunction.setup_logger('Watchdog','.\\Logs\\Watchdog.log',level=logging.INFO,formatter='%(asctime)s : %(name)s : %(levelname)-8s : %(message)s')

## Start messages
loggerwatchdog.info("******************** Pre-initialization ********************")

## This checks if the directories you have entered are valid. If not it will create them
for directory in (DIRECTORY_TO_WATCH,DIRECTORY_TO_MOVE,DIRECTORY_UNMATCHED):
    if os.path.exists(directory):
        loggerwatchdog.info("Directory exists. Don't need to create: " +directory)
        pass
    else:
        loggerwatchdog.info("Directory doesn't exist. Will try to create: " +directory)
        try:
            os.mkdir(directory)
        except OSError:
            loggerwatchdog.info ("Error creating directory: " +directory) 
        else:
            loggerwatchdog.info ("Directory created successfully: " +directory)


loggerwatchdog.info("Watchdog will be active to this directory: "+DIRECTORY_TO_WATCH)
loggerwatchdog.info("Watchdog will move the files to this directory: " +DIRECTORY_TO_MOVE)
loggerwatchdog.info("Preferred ID is set to: " +str(pref_ID))
loggerwatchdog.info("Dry Run is set to: " +str(pref_DryRun))
loggerwatchdog.info("******************** Watchdog initiated ********************")

## The watcher class code
class Watcher:

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            loggerwatchdog.info ("Watchdog disabled")

        self.observer.join()

## The handler class code
class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            ## Take any action here when a file is first created.
            loggerwatchdog.info ("Received created event : %s" % event.src_path)

        ##elif ((event.event_type == 'created') or event.event_type == 'modified'):
        elif event.event_type == 'modified':
            ## Taken any action here when a file is modified.
            loggerwatchdog.info ("Received modified event: %s" % event.src_path)
            new_filename = None
            if os.path.exists(event.src_path):
                siteDirectory = os.path.dirname(event.src_path)
                siteFolder = os.path.basename(siteDirectory)
                complete_filename = os.path.basename(event.src_path)
                filename_title = os.path.splitext(complete_filename)[0]
                filename_type = os.path.splitext(complete_filename)[1]
                filename_size = os.stat(event.src_path).st_size
                if ((filename_type in ('.mp4','.mkv','.avi')) and (filename_size > 15000000)):
                    loggerwatchdog.info ("Processing filename %s which is a type of %s" % (filename_title, filename_type))
                    loggerwatchdog.info("The file was placed at folder: " +siteFolder)
                    trashTitle = ('RARBG', 'COM', '\d{3,4}x\d{3,4}', 'HEVC', 'H265', 'AVC', '\dK', '\d{3,4}p', 'TOWN.AG_', 'XXX', 'MP4', 'KLEENEX', 'SD', '1080p', '720p', '480p', '360p')
                    filename_title = re.sub(r'\W', ' ', filename_title)
                    for trash in trashTitle:
                        filename_title = re.sub(r'\b%s\b' % trash, '', filename_title, flags=re.IGNORECASE)
                    filename_title = ' '.join(filename_title.split())
                    loggerwatchdog.info ("Filename after initial process: " +filename_title)
                    loggerwatchdog.info ("************ Process with PAsearchSites follows ************")
                    searchSettings = PAsearchSites.getSearchSettings(filename_title)
                    searchTitle = searchSettings[1]
                    searchDate = searchSettings[2]
                    loggerwatchdog.info ("searchTitle (after date processing): " +searchTitle)
                    if (searchDate != None):
                        loggerwatchdog.info ("searchDate Found: " +searchDate)
                    else:
                        loggerwatchdog.info ("File didn't contain Date information. If this is false check the RegEx at PASearchSites for Dates")
                    loggerwatchdog.info ("****************** PAsearchSites matching ******************")
                    loggerwatchdog.info("Use PAsearchSites to match %s folder with a supported PA Site ID" %siteFolder)
                    siteID = None
                    siteID = PAsearchSites.getSearchSiteIDByFilter(siteFolder)
                    if (siteID != None):
                        siteName = PAsearchSites.getSearchSiteName(siteID)
                        siteBaseURL = PAsearchSites.getSearchBaseURL(siteID)
                        siteSearchURL = PAsearchSites.getSearchSearchURL(siteID)
                        loggerwatchdog.info("PA Site ID: %d" %siteID)
                        loggerwatchdog.info("PA Site Name: %s" %siteName)
                        loggerwatchdog.info("PA Site Base URL: %s" %siteBaseURL)
                        loggerwatchdog.info("PA Site Search URL: %s" %siteSearchURL)
                        ## All sites that are under the network1service this would be more clear at the future
                        if ((siteID == 2) or (54 <= siteID <= 80) or (137 <= siteID <= 182) or (261 <= siteID <= 276) or (288 <= siteID <= 291) or (siteID == 328) or (333 <= siteID <= 340) or (361 <= siteID <= 364) or (397 <= siteID <= 407) or (582 <= siteID <= 583) or (siteID == 690) or (siteID == 733) or (737 <= siteID <= 740) or (siteID == 759) or (siteID == 768) or (798 <= siteID <= 799) or (802 <= siteID <= 806) or (808 <= siteID <= 809) or (822 <= siteID <= 828) or (siteID == 841) or (siteID == 852) or (859 <= siteID <= 860) or (siteID == 872) or (siteID == 876)):
                            new_filename = renamer_network1service.rename(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate,filename_type,pref_ID)
                        elif ((83 <= siteID <= 135)):
                            new_filename = renamer_sitebangbros.rename(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate,filename_type,pref_ID)
                        if (pref_DryRun == False):
                            if (new_filename != None):
                                if (os.path.exists(DIRECTORY_TO_MOVE+'\\'+siteFolder+'\\')):
                                    loggerwatchdog.info("The site sub-folder was detected to %s location. Try to move %s there" % (DIRECTORY_TO_MOVE,new_filename))
                                    try:
                                        os.rename(event.src_path,r''+DIRECTORY_TO_MOVE+'\\'+siteFolder+'\\'+new_filename)
                                    except OSError:
                                        loggerwatchdog.info ("There was an error moving %s file to %s location" % (new_filename,DIRECTORY_TO_MOVE))
                                    else:
                                        loggerwatchdog.info ("Successfully moved %s to %s location" % (new_filename,DIRECTORY_TO_MOVE))
                                else:
                                    loggerwatchdog.info("Couldn't detect site sub-folder to %s location. Try to create site's sub-folder and move the %s file there" % (DIRECTORY_TO_MOVE,new_filename))
                                    try:
                                        os.mkdir(DIRECTORY_TO_MOVE+'\\'+siteFolder+'\\')
                                        os.rename(event.src_path,r''+DIRECTORY_TO_MOVE+'\\'+siteFolder+'\\'+new_filename)
                                    except OSError:
                                        loggerwatchdog.info ("There was an error moving %s file to %s location" % (new_filename,DIRECTORY_TO_MOVE))
                                    else:
                                        loggerwatchdog.info ("Successfully created %s directory and move %s file there" % (DIRECTORY_TO_MOVE,new_filename))
                            else:
                                os.rename(event.src_path,r''+DIRECTORY_UNMATCHED+'\\'+complete_filename)
                                loggerwatchdog.info("Couldn't match scene. Moved to the Unmatched folder")
                        else:
                            loggerwatchdog.info("Dry run is enabled!!!")
                            if (new_filename != None):
                                loggerwatchdog.info("Your scene was matched and could be renamed to: " +new_filename)
                                loggerwatchdog.info("Disable dry run to do so")
                            else:
                                loggerwatchdog.info("Couldn't match scene. Scene should have moved to Unmatched folder")
                                loggerwatchdog.info("Disable Dry Run to do so") 
                    else:
                        loggerwatchdog.info("Couldn't found %s site to the PAsearchSites array" %siteFolder)
                        if (pref_DryRun == False):
                            os.rename(event.src_path,r''+DIRECTORY_UNMATCHED+'\\'+complete_filename)
                            loggerwatchdog.info("Scene was moved to the Unmatched folder")
                        else:
                            loggerwatchdog.info("Dry run is enabled!!!")
                            loggerwatchdog.info("Scene should have moved to Unmatched folder")
                            loggerwatchdog.info("Disable Dry Run to do so") 
                else:
                    pass
        elif event.event_type == 'deleted':
            ## Taken any action here when a file is deleted.
            loggerwatchdog.info ("Received deleted event: %s" % event.src_path)

if __name__ == '__main__':
    w = Watcher()
    w.run()