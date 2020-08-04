## Dependencies
import time
import requests
import json
import logging
import enchant
## Other .py files

## Logger information
logger = logging.getLogger('Renamers')

## Get cookies function
def get_Cookies(url):
    req = requests.get(url)

    return req.cookies

def rename(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate,filename_type,pref_ID):
    cookies = get_Cookies(siteBaseURL)
    searchTitle = searchTitle.split("_")[0]
    splited = searchTitle.split(' ')[0]
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
        ## The below line logger.infos the json. You can comment it out to see the retrieved information and for debugging
        ##logger.info (searchResults)
        ScenesQuantity = len(searchResults)
        logger.info("Possible matching scenes found in results: " +str(ScenesQuantity))
        ## Make a Matrix to store our results and then sort it via a score function
        ResultMatrix = [[0 for x in range(6)] for y in range(ScenesQuantity)]
        x = 0
        for searchResult in searchResults:
            curActorstring = ''
            ResultMatrix[x][0] = curID = str(searchResult['id'])
            ResultMatrix[x][1] = curTitle = searchResult['title']
            ResultMatrix[x][2] = curDate = searchResult['dateReleased'].split("T")[0]
            actorssize = len(searchResult['actors'])
            for i in range(actorssize):
                actor = searchResult['actors'][i]['name']
                curActorstring += actor+' & '
            ResultMatrix[x][3] = curActorstring[:-3]
            curSubsite = ''
            if 'collections' in searchResult and searchResult['collections']:
                curSubsite = searchResult['collections'][0]['name']
            ResultMatrix[x][4] = curSubsite
            if (searchTitle.isdigit()):
                ResultMatrix[x][5] = curScore = 100 - enchant.utils.levenshtein(searchTitle, curID)
            elif searchDate:
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
        if (pref_ID == True):
            new_filename = siteName+' - '+ID
        else:
            if (Actors != '' and Subsite != ''): ## We have information for actors and subsite
                new_filename = siteName+' - '+Title+' - '+Date+' - '+Actors +' - '+Subsite+filename_type
            elif (Actors != '' and Subsite == ''): ## We have information for actors and not for subsite
                new_filename = siteName+' - '+Title+' - '+Date+' - '+Actors +filename_type
            elif (Actors == '' and Subsite == ''): ## We don't have information for actors and subsite
                new_filename = siteName+' - '+Title+' - '+Date+filename_type
            elif (Actors == '' and Subsite != ''): ## We don't have information for actors but we have for subsite
                new_filename = siteName+' - '+Title+' - '+Date+' - '+Subsite+filename_type
        ## logger.info new filename
        logger.info ("*************** After-Process filename section *************")
        logger.info ("The new filename is: " +new_filename)
        logger.info ("******************** Return to Watchdog ********************")
    except:
        new_filename = None
    return new_filename