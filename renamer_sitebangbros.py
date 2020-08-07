## Dependencies
import time
import requests
import json
import logging
import enchant
from lxml import html
import datetime
## Other .py files
import LoggerFunction

## Basic Logger information
logger = LoggerFunction.setup_logger('Renamers', '.\\Logs\\Watchdog.log',logging.INFO,formatter='%(asctime)s : %(name)s : %(levelname)-8s : %(message)s')

def rename(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate,filename_type,pref_ID):
    ## Scene Logger information
    SceneNameLogger = LoggerFunction.setup_logger('SceneNameLogger', '.\\Logs\\'+searchTitle+'.log',level=logging.DEBUG,formatter='%(message)s')
    splited = searchTitle.split(' ')[0]
    if (splited.isdigit()):
        sceneID = splited
    else:
        sceneID = None
    if (sceneID != None):
        print (sceneID)
        URL = (siteSearchURL + sceneID + "/1")
    else:
        URL = (siteSearchURL + searchTitle.replace(" ","-") + "/1")
    logger.info ("******************** URL used section **********************")
    logger.info (URL)
    req = requests.get(siteSearchURL + searchTitle + "/1")
    HTMLResponse = html.fromstring(req.content)
    searchResults = HTMLResponse.xpath('//div[@class="thumbsHolder elipsTxt"]/div[1]/div[@class="echThumb"]')
    ScenesQuantity = len(searchResults)
    logger.info("Possible matching scenes found in results: " +str(ScenesQuantity))
    ResultsMatrix = [['0','0','0','0','0',0]]
    try:
        for searchResult in searchResults:
            if searchResult.xpath('.//a[contains(@href, "/video")]'):
                curSubsite = ''
                curActorstring = ''
                curID = searchResult.xpath('.//a[contains(@href, "/video")]//@href')[0].replace("/video","").split("/")[0]
                curTitle = searchResult.xpath('.//a[contains(@href, "/video")]/@title')[0].replace(":"," ")
                curDate = datetime.datetime.strptime(str(searchResult.xpath('.//span[@class="faTxt"]')[1].text_content().strip()),'%b %d, %Y').strftime('%Y-%m-%d')
                curSubsite = searchResult.xpath('.//span[@class="faTxt"]')[0].text_content().strip()
                actorssize = len(searchResult.xpath('.//div[contains(@class, "cast-wrapper")]/a'))
                for i in range(actorssize):
                    actor = searchResult.xpath('.//div[contains(@class, "cast-wrapper")]/a')[i].text_content().strip()
                    curActorstring += actor+' & '
                curActorstring = curActorstring[:-3]
                if (sceneID != None):
                    curScore = 100 - enchant.utils.levenshtein(sceneID, curID)
                elif (searchDate != None):
                    curScore = 100 - enchant.utils.levenshtein(searchDate, curDate)
                else:
                    curScore = 100 - enchant.utils.levenshtein(searchTitle.lower(), curTitle.lower())
                SceneNameLogger.debug ("************** Current Scene Matching section **************")
                SceneNameLogger.debug ("ID: " +curID)
                SceneNameLogger.debug ("Title: " +curTitle)
                SceneNameLogger.debug ("Date: " +curDate)
                SceneNameLogger.debug ("Actors: " +curActorstring)
                SceneNameLogger.debug ("Subsite: " +curSubsite)
                SceneNameLogger.debug ("Score: " +str(curScore))
                ResultsMatrix.append([curID, curTitle, curDate, curActorstring, curSubsite, curScore])
        ResultsMatrix.sort(key=lambda x:x[5],reverse=True)
        ## Calculate new filename section using sorted ResultsMatrix
        ID = ResultsMatrix[0][0]
        Title = ResultsMatrix[0][1]
        Date = ResultsMatrix[0][2]
        Actors = ResultsMatrix[0][3]
        Subsite = ResultsMatrix[0][4]
        if (pref_ID == True):
            new_filename = siteName+' - '+ID+filename_type
            SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
            SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
            for y in range (ScenesQuantity):
                SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][0])
            SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
        else:
            if (Actors != '' and Subsite != ''): ## We have information for actors and Subsite
                new_filename = siteName+' - '+Title+' - '+Date+' - '+Actors +' - '+Subsite+filename_type
            elif (Actors != '' and Subsite == ''): ## We have information for actors and not for Subsite
                new_filename = siteName+' - '+Title+' - '+Date+' - '+Actors +filename_type
            elif (Actors == '' and Subsite == ''): ## We don't have information for actors and Subsite
                new_filename = siteName+' - '+Title+' - '+Date+filename_type
            elif (Actors == '' and Subsite != ''): ## We don't have information for actors but we have for Subsite
                new_filename = siteName+' - '+Title+' - '+Date+' - '+Subsite+filename_type
            SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
            SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
            for y in range (ScenesQuantity):
                SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][1]+' - '+ResultsMatrix[y][2])
            SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
        ## logger.debug new filename
        logger.info ("*************** After-Process filename section *************")
        logger.info ("The new filename is: " +new_filename)
        logger.info ("******************** Return to Watchdog ********************")
    except:
        new_filename = None
    return new_filename