## Dependencies
import time
import requests
import json
import logging
import enchant
from lxml import html
import datetime
## Other .py files

## Logger information
logger = logging.getLogger('Renamers')

def rename(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate,filename_type,pref_ID):
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
    ResultMatrix = [[0 for x in range(6)] for y in range(ScenesQuantity)]
    x = 0
    try:
        for searchResult in searchResults:
            if searchResult.xpath('.//a[contains(@href, "/video")]'):
                curSubsite = ''
                curActorstring = ''
                ResultMatrix[x][0] = curID = searchResult.xpath('.//a[contains(@href, "/video")]//@href')[0].replace("/video","").split("/")[0]
                ResultMatrix[x][1] = curTitle = searchResult.xpath('.//a[contains(@href, "/video")]/@title')[0].replace(":"," ")
                ResultMatrix[x][2] = curDate = datetime.datetime.strptime(str(searchResult.xpath('.//span[@class="faTxt"]')[1].text_content().strip()),'%b %d, %Y').strftime('%Y-%m-%d')
                curSubsite = searchResult.xpath('.//span[@class="faTxt"]')[0].text_content().strip()
                actorssize = len(searchResult.xpath('.//div[contains(@class, "cast-wrapper")]/a'))
                for i in range(actorssize):
                    actor = searchResult.xpath('.//div[contains(@class, "cast-wrapper")]/a')[i].text_content().strip()
                    curActorstring += actor+' & '
                ResultMatrix[x][3] = curActorstring[:-3]
                ResultMatrix[x][4] = curSubsite
                if (sceneID != None):
                    ResultMatrix[x][5] = curScore = 100 - enchant.utils.levenshtein(sceneID, curID)
                elif (searchDate != None):
                    ResultMatrix[x][5] = curScore = 100 - enchant.utils.levenshtein(searchDate, curDate)
                else:
                    ResultMatrix[x][5] = curScore = 100 - enchant.utils.levenshtein(searchTitle.lower(), curTitle.lower())
                logger.info ("************** Current Scene Matching section **************")
                logger.info ("ID: " +curID)
                logger.info ("Title: " +curTitle)
                logger.info ("Date: " +curDate)
                logger.info ("Actors: " +curActorstring[:-3])
                logger.info ("Subsite: " +curSubsite)
                logger.info ("Score: " +str(curScore))
                x = x+1
        ResultMatrix.sort(key=lambda x:x[5],reverse=True)
        logger.info ("This is the list with the first item being the most matched with the scene. Use those to rename the file!")
        logger.info (ResultMatrix)
        ## Calculate new filename section using sorted ResultMatrix
        ID = ResultMatrix[0][0]
        Title = ResultMatrix[0][1]
        Date = ResultMatrix[0][2]
        Actors = ResultMatrix[0][3]
        Subsite = ResultMatrix[0][4]
        if (Actors != '' and Subsite != ''): ## We have information for actors and Subsite
            if (pref_ID == True):
                new_filename = siteName+' - '+ID+filename_type
            else:
                new_filename = siteName+' - '+Title+' - '+Date+' - '+Actors +' - '+Subsite+filename_type
        elif (Actors != '' and Subsite == ''): ## We have information for actors and not for Subsite
            if (pref_ID == True):
                new_filename = siteName+' - '+ID+filename_type
            else:
                new_filename = siteName+' - '+Title+' - '+Date+' - '+Actors +filename_type
        elif (Actors == '' and Subsite == ''): ## We don't have information for actors and Subsite
            if (pref_ID == True):
                new_filename = siteName+' - '+ID+filename_type
            else:
                new_filename = siteName+' - '+Title+' - '+Date+filename_type
        elif (Actors == '' and Subsite != ''): ## We don't have information for actors but we have for Subsite
            if (pref_ID == True):
                new_filename = siteName+' - '+ID+filename_type
            else:
                new_filename = siteName+' - '+Title+' - '+Date+' - '+Subsite+filename_type
        ## logger.info new filename
        logger.info ("*************** After-Process filename section *************")
        logger.info ("The new filename is: " +new_filename)
        logger.info ("******************** Return to Watchdog ********************")
    except:
        new_filename = None
    return new_filename