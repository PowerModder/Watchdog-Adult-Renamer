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
import GoogleSearchFunction

def search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate,WorkingDir):
    ## Basic Log Configuration
    logger = LoggerFunction.setup_logger('Searcher', WorkingDir+'\\Logs\\Watchdog.log',level=logging.INFO,formatter='%(asctime)s : %(name)s : %(levelname)-8s : %(message)s')
    ## Scene Logger information
    SceneNameLogger = LoggerFunction.setup_logger('SceneNameLogger', WorkingDir+'\\Logs\\'+searchTitle+'.log',level=logging.DEBUG,formatter='%(message)s')
    ResultsMatrix = [['0','0','0','0','0',0]]
    ScenesURL = []
    if ('vs' in searchTitle):
        DirectURL = (siteSearchURL + searchTitle.replace(" ","-") + '.html')
        ScenesURL.append(DirectURL)
    googleResults = GoogleSearchFunction.getFromGoogleSearch(searchTitle, siteSearchURL, WorkingDir)
    for searchURL in googleResults:
        if (searchURL not in ScenesURL):
            ScenesURL.append(searchURL)
    logger.info("Possible matching scenes found in results: " +str(len(ScenesURL)))
    for SceneURL in ScenesURL:
        try:
            logger.info ("******************** URL used section **********************")
            logger.info (SceneURL)
            req = requests.get(SceneURL)
            HTMLResponse = html.fromstring(req.content)
            curID = ''
            curDate = ''
            curActorstring = ''
            curSubsite = ''
            curTitle = (HTMLResponse.xpath('//title')[0].text_content().strip()).replace("Mixed Wrestling","")
            try:
                curDate = datetime.datetime.strptime(str(HTMLResponse.xpath('//span[(contains(@class, "update_date"))]')[0].text_content().strip()),'%m/%d/%Y').strftime('%Y-%m-%d')
            except:
                pass
            actorssize = len(HTMLResponse.xpath('//div/span[@class="tour_update_models"]/a'))
            for i in range(actorssize):
                actor = HTMLResponse.xpath('//div/span[@class="tour_update_models"]/a')[i].text_content().strip()
                curActorstring += actor+' vs '
            curActorstring = curActorstring[:-3]
            if ((searchDate != None) and (curDate != '')):
                curScore = 100 - enchant.utils.levenshtein(searchDate, curDate)
            else:
                curScore = 100 - enchant.utils.levenshtein(searchTitle.lower(), curTitle.lower())
            SceneNameLogger.debug ("************** Current Scene Matching section **************")
            SceneNameLogger.debug ("ID: Site doesn't provide sceneID information")
            SceneNameLogger.debug ("Title: " +curTitle)
            SceneNameLogger.debug ("Date: " +curDate)
            SceneNameLogger.debug ("Actors: " +curActorstring)
            SceneNameLogger.debug ("Subsite: Site doesn't provide Subsite information")
            SceneNameLogger.debug ("Score: " +str(curScore))
            ResultsMatrix.append([curID, curTitle, curDate, curActorstring, curSubsite, curScore])
        except:
            pass
    ResultsMatrix.sort(key=lambda x:x[5],reverse=True)
    logger.info ("*************** Moving to Renamer Function *****************")
    SceneNameLogger.handlers.pop()
    logger.handlers.pop()
    return ResultsMatrix