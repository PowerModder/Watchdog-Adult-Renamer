## Dependencies
import time
import requests
import json
import logging
import enchant
## Other .py files
import LoggerFunction

## Basic Logger information
logger = LoggerFunction.setup_logger('Renamers', '.\\Logs\\Watchdog.log',logging.INFO,formatter='%(asctime)s : %(name)s : %(levelname)-8s : %(message)s')

## Get cookies function
def get_Cookies(url):
    req = requests.get(url)

    return req.cookies

def rename(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate,filename_type,pref_ID):
    ## Scene Logger information
    SceneNameLogger = LoggerFunction.setup_logger('SceneNameLogger', '.\\Logs\\'+searchTitle+'.log',level=logging.DEBUG,formatter='%(message)s')
    cookies = get_Cookies(siteBaseURL)
    searchTitle = searchTitle.split("_")[0]
    splited = searchTitle.split(' ')[0]
    sceneID = None
    if (splited.isdigit()):
        sceneID = splited[0]
        searchTitle = searchTitle.replace(splited, '', 1).strip()
        URL = siteSearchURL+'/v2/releases?type=scene&id='+splited
    else:
        URL = siteSearchURL+'/v2/releases?type=scene&search='+searchTitle
    ## Scene matching section
    logger.info ("******************** URL used section **********************")
    logger.info (URL)
    page = requests.get(URL,headers={'Instance': cookies['instance_token']})
    try:
        searchResults = page.json()['result']
        ## The below line logger.debugs the json. You can comment it out to see the retrieved information and for debugging
        ##logger.debug (searchResults)
        ScenesQuantity = len(searchResults)
        logger.info("Possible matching scenes found in results: " +str(ScenesQuantity))
        ## Make a Matrix to store our results and then sort it via a score function
        ResultsMatrix = [['0','0','0','0','0',0]]
        for searchResult in searchResults:
            curActorstring = ''
            curID = str(searchResult['id'])
            curTitle = searchResult['title']
            curDate = searchResult['dateReleased'].split("T")[0]
            actorssize = len(searchResult['actors'])
            for i in range(actorssize):
                actor = searchResult['actors'][i]['name']
                curActorstring += actor+' & '
            curActorstring = curActorstring[:-3]
            curSubsite = ''
            if 'collections' in searchResult and searchResult['collections']:
                curSubsite = searchResult['collections'][0]['name']
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
        ## Calculate new filename section using sorted ResultMatrix
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