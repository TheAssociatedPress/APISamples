#!/usr/bin/env python
import requests
import copy
import time
import re
import json
import httplib
import pprint

from datetime import datetime
import sys
import getopt
import os
from string import Template
import re

requests.packages.urllib3.disable_warnings()

TmpDataDir="./mediaapi_output_tmp"           #
if not os.path.exists(TmpDataDir):
    os.makedirs(TmpDataDir)

#### Command-line options/defaults

Action = 'feed'
ActionList = [ 'feed', 'search' ]

ExtraFeedParams = 'q=mindate:>now-3d'
ExtraFeedParams = ''
ExtraSearchParams = ''
TestType="feed"
FollowNext=False
LastSize=0
Verbose=False
ApiKey="<Enter-APIKEY>"

BaseHTTPHeaders = { 
    'User-Agent' : 'APMediaApi-Demo-2.0'
    , 'x-api-key' : ApiKey}


ProcessFeed=False
ProcessRenditions=False
ProcessAssociations=False
HttpScheme="https"
MaxLoops=1

SessionId=os.getpid()

#### Metrics
HttpErrorCount=0
rqNumber=0
rqTimeLabel="xxx"
TotalBytes=0
TotalTime=0.0

rqFileData=""

MediaAPIBaseURL = "api.ap.org/media/v"

UsageMsg="\n" \
         "Usage: tstKapi ...[options]...\n" \
        "   -k <ApiKey>         Use <ApiKey>\n" \
        "   -f                  Follow Next-Pages (search&feed), otherwise process 2nd level tests\n" \
        "   -v                  Verbose\n" +\
        Template("   -A <action>         Action $act \n").substitute(act = ActionList ) + \
        "   -d                  Display Defaults (-k, -a, -p) \n" \
        "   -P                  Process Feed entries\n" \
        "   -R                  Process (download) Rendition entries (implies -P)\n" \
        "   -a                  follow (process) Associations \n" +\
        "   -r <##>             Repeat the request (or Follow next-links) ## times\n" + \
        Template("   -q <query_params>   Add <query_params> to request \n").substitute( qqq = ExtraSearchParams )

def usageMessageExit ( withError = None ):
    if withError:
        print "Error: ", withError
    print "\n", UsageMsg
    exit ( 2 )


if len(sys.argv) < 2:
    usageMessageExit()
    exit(2)

optlist, args = getopt.getopt( sys.argv[1:], 'RvfPadq:k:r:A:')

for o,a in optlist:
    if o == "-k":
        ApiKey = a
    elif o == "-P":
        ProcessFeed = True
    elif o == "-R":
        ProcessRenditions = ProcessFeed = True
    elif o == "-f":
        FollowNext=True
    elif o == "-a":
        ProcessAssociations=True
    elif o == "-A":
        if a in ActionList:
            Action = a
        else:
            usageMessageExit( "Action(-A) param '{}' must be one of {}".format(a, ActionList))
    elif o == "-r":
        if a.isdigit():
            MaxLoops = int(a)
        else:
            usageMessageExit ( "Repeat#(-r) param '{}' must be a decimal integer ".format(a) )
    elif o == "-v":
        Verbose=True
    elif o == "-d":
        Action = "ShowDefaults"
    elif o == "-q":
        ExtraSearchParams = a
        ExtraFeedParams = a
    else:
        usageMessageExit ( "Unknown option: " + o )

serverBase = HttpScheme + '://' + MediaAPIBaseURL
getAllSearchBase = serverBase + '/content/search?q=type:picture+AND+tokyo&page_size=5'
getAllSearchBase = serverBase + '/content/search?q=type:text&page_size=5'
getAllSearchBase = serverBase + '/content/search?q=yosemite&page_size=50'

getAllFeedBase = serverBase + '/content/feed?q=productid:2&exclude=renditions.main'
getAllFeedBase = serverBase + '/content/feed?q=productid:31990+AND+mindate:>now-3d&page_size=5&exclude=renditions.main'
getAllFeedBase = serverBase + '/content/feed'

if ExtraSearchParams != '':
    getAllSearchBase += ('&' if '?' in getAllSearchBase else '?') + ExtraSearchParams

if ExtraFeedParams != '':
    getAllFeedBase += ('&' if '?' in getAllFeedBase else '?') + ExtraFeedParams

fetchFeedLink = getAllFeedBase
fetchSearchLink = getAllSearchBase

nextLink = None

if Action == "ShowDefaults":
    print "\nDefaults:"
    print "apikey(k): {}".format(ApiKey)
    print "base(default) /feed   : {}".format(getAllFeedBase)
    print "base(default) /search : {}".format(getAllSearchBase)
    exit(0)

emptyCount = 0
rqNumber = 0
lastNextLink = "unlikely"
nextLink = ""
downloadStats = {}

###
# /content/search and /content/feed return a common JSON structure, this function handles both
# structure: { misc_envelope_header_info, data { items [ { meta:{} item:{} }, ..... ] }
###
def processSearchOrFeedRespsone(feedBody):
    global nextLink
    nextLink = None
    js = json.loads(feedBody)
    rqId = js.get('id')
    if js.get('error'):
        print "ERROR: Check feed/search request, received error: {}".format(js.get('error'))

    dataBlock = js.get('data')
    if dataBlock is not None:
        pageType = "next_page"
        next_page = dataBlock.get('next_page')
        itemsBlock = dataBlock.get('items')
        num_items = len(itemsBlock)
        if next_page is None:   # Never happens from /feed
            # NOTE: Only in /search responses, when reaching the "end" a 'feed_href' link may be provided that lets you
            # transition to a /feed model, continuing to monitor for newly arriving content matching your initial /search
            next_page = dataBlock.get('feed_href')
            if next_page is not None:
                pageType = "feed_href"

        print "processEntireFeed - Response with id:{} items:{} {}:{}".format(rqId, num_items, pageType, next_page)

        if ProcessFeed:
            processAllItems(itemsBlock)

        nextLink = next_page

        if pageType == "feed_href":
            print "\nprocessEntireFeed - Reached end of /search results, feed_href provided to transition to /feed ..."
        elif next_page is None:
            print "\nprocessEntireFeed - WARNING: Body has no next_page or feed_href"

def processAllItems(items):
    localEntry = 0
    for metaItem in items:
        process1metaItem( TmpDataDir, metaItem, localEntry)
        localEntry += 1

    #print "End of {} Feed Entries.  Download stats:\n".format(localEntry)

def process1metaItem( baseDir, metaItem, entryIndex ):
    item = metaItem.get('item')
    altids = item.get('altids')
    iid = altids.get('itemid')
    etag = altids.get('etag')
    version = item.get('version')
    type = item.get('type')
    headline = item.get('headline')
    if headline is None:
        headline = ''
    associations = item.get('associations')
    associations_len = 0
    if associations != None:
        associations_len = len(associations)
    renditions = item.get('renditions')
    renditions_len = len(renditions) if renditions != None else 0
    entryDir = baseDir + "/" + "{}-{}_{}".format(iid, version, type)

    if not os.path.exists(entryDir):
        os.makedirs(entryDir)

    entryFile = "{}/metadata_{}-{}_{}.json".format(entryDir, iid, version, type)
    with open(entryFile, 'wb') as fEntry:
        fEntry.write(json.dumps(metaItem, indent = 4))
        fEntry.closed

    feTag = "{}.{}".format(iid, version )   # was entryIndex.iid
    print "\nEntry[{}] :: itemid:{} type:{} headline:\"{}\" renditions:{} associations:{} ".format( entryIndex, feTag,
                                                                    type,headline.encode('utf-8'),
                                                                    renditions_len, associations_len )

    if ProcessAssociations and associations != None:
        for assocName in associations:
            assoc = associations[assocName]
            print "\tassociations.{} type:{} uri:{}".format(assocName, assoc.get('type'), assoc.get('uri'))
            issueItemRequest( entryDir, assoc.get('uri'), assoc)

    if renditions != None:
        for rendName in renditions:
            rend = renditions[rendName]
            rendHref = rend.get('href')
            if rendHref is None:    # No href if unavailable for download
                continue
            if rend.get('priced'):
                rendPricetag = rend.get('pricetag')
                ## WARNING: Uncomment following line to supply price-acknowledgement on a priced(charged) download
                ## Not acknowledging will result in a download error(e.g. "402 - Payment Required") when following the link
                #rendHref = rendHref + "&pricetag={}".format(rendPricetag)
                if ProcessRenditions:
                    print "\t(WARNING) renditions.{} priced:true must ACKNOWLEDGE by appending '&pricetag={}'".format(rendName, rendPricetag )
            rendExt = rend.get('fileextension')
            feTag = "{}_{}.{}".format( rendName, rend.get('contentid'), rendExt)
            allV = rend.get('version_links')        # If you use /feed?versions=all you should be prepared to iterate on this array of anpa links
            if Verbose and not ProcessRenditions:
                print "\trenditions.{}\t href:{}".format(rendName, rendHref)
            if ProcessRenditions:
                issueDownloadRequest(entryDir, rendHref, rendName, rendExt, feTag )

###
# Call HTTP GET on /content/search or /content/feed
# After an initial request, gathering more results is just a matter of
# following the returned 'next_page' link
###
def issueSearchOrFeedRequest(forLink):
    if re.match('apikey=', forLink):
        oneLink = forLink
    elif forLink.find('?') > 0:
        oneLink = forLink + '&apikey={}'.format(ApiKey)
    else:
        oneLink = forLink + '?apikey={}'.format(ApiKey)

    print "\nNow:{} Test-request: {}".format( str(datetime.now().time()).rstrip('0'), oneLink )

    return requests.get(oneLink, headers=BaseHTTPHeaders,
                       timeout = 40.0,      # You should allow for /feed requests sometimes taking ~30 seconds
                       verify=False )       # TIP: Requests GZIP encoding by default, you should too!

###
# Request full metadata for one specific itemid
# Used to:
#   1) Follow an 'associations' link to get metadata for related content
#   2) Fetch more (or all) metadata than that originally returned by /search or /feed
#   3) Refresh/update previously fetched metadata
###
def issueItemRequest( parentDir, assocUri, assoc):
    global downloadStats, HttpErrorCount
    if re.match('apikey=', assocUri):
        oneLink = assocUri
    else:
        oneLink = assocUri + '&apikey={}'.format(ApiKey)

    assocIid = assoc.get('altids').get('itemid')
    assocType = assoc.get('type')
    assocDir = parentDir + "/association_{}_{}".format(assocType, assocIid)

    assocEtag = assoc.get('altids').get('etag')     # TIP: Use with {itemid} to check local cache
    print " -- Association:{} etag:{}".format(assocIid, assocEtag)

    RqHeads = copy.copy(BaseHTTPHeaders)
    r = requests.get(oneLink, headers=RqHeads, verify=False, timeout = 40.0 )
    statusMsg = httplib.responses[r.status_code]
    if not r.status_code in downloadStats:
        downloadStats[r.status_code] = 0
    downloadStats[r.status_code] += 1
    if r.status_code < 300:
        statusBody = ""
        respBody = json.loads(r.text)
        respData = respBody.get('data')
        process1metaItem( parentDir, respData, 0)
    else:
        print " -- Association.GET Failed: status={}/{} url:{}".format(r.status_code, r.reason, oneLink)
        HttpErrorCount += 1

###
# Issue HTTP GET for an asset (rendition)
# Note: <apikey> is added to these links for authentication
# Note: Must be prepared to follow a returned redirect request
# Note: Consider capturing returned HTTP Headers for main's (not demonstrated)
###
def issueDownloadRequest( toDir, forLink, ofType, withExt, forEntry = 'standalone'):
    global downloadStats, HttpErrorCount, TotalBytes
    if re.match('apikey=', forLink):
        oneLink = forLink
    else:
        oneLink = forLink + '&apikey={}'.format(ApiKey)

    rqTimeLabel = str(datetime.now().time()).rstrip('0')
    dldResp = requests.get(oneLink, headers=BaseHTTPHeaders, verify=False, stream=True,
                          allow_redirects = True,   ## When downloading renditions it's essential to follow redirects
                          timeout = 40.0  )
    if not dldResp.status_code in downloadStats:
        downloadStats[dldResp.status_code] = 0
    downloadStats[dldResp.status_code] += 1
    if dldResp.status_code > 302:
        HttpErrorCount += 1
    showLink = " code:{} from GET: {}".format(dldResp.status_code, oneLink) if Verbose or dldResp.status_code > 302 else ""
    print "  rendition.{} DOWNLOAD status:{} {}".format(ofType, dldResp.reason, showLink)
    if dldResp.url:
        if dldResp.history and dldResp.history[0].status_code:
            redirStatus = dldResp.history[0].status_code
            if redirStatus != 301:
                print "  [ auto-redirect status:{} ]".format( redirStatus)

    rqFileData = toDir + "/" + forEntry

    rawLen = 0
    with open ( rqFileData, 'wb') as rawFile:
        while True:
            awp = dldResp.raw.read(4096, decode_content=True)
            if awp is None or awp == "":
                break
            rawLen += len(awp)
            rawFile.write(awp)
        rawFile.closed

    print "    .. saved-as:{} bytes:{}".format(rqFileData, rawLen )
    TotalBytes += rawLen


if Action == "feed" or Action == "search":
    TestType = Action
    fetchLink = fetchFeedLink if Action == "feed" else fetchSearchLink
    fetchLinkInitial = fetchLink
    for rqNumber in xrange(1,MaxLoops+1):
        rqTimeLabel = str(datetime.now().time()).rstrip('0')
        rqFileBase =  TmpDataDir + "/{}-{}-{}_{}_{}".format( rqTimeLabel, TestType, ApiKey, SessionId, rqNumber ).replace(":","")
        rqFileData = rqFileBase + "_data.json"
        r = issueSearchOrFeedRequest(fetchLink)
        h = r.headers

        with open(rqFileData, 'wb') as f:            # 'b' to stop cr/lf manip
            f.write(r.content)
            f.closed

        processSearchOrFeedRespsone(r.text)
        if nextLink != None:
            fetchLink = nextLink

        if FollowNext and nextLink != None:
            if nextLink != lastNextLink:
                print "Nextlink {}".format(nextLink)
                lastNextLink = nextLink
            else:
                print "No nextlink change"

    print "Completed %d %s cycles.  HttpErrors:%d  Kb:%.2f  Download HTTP status code summary:" % ( rqNumber, Action, HttpErrorCount, TotalBytes/(1024))
    for key, value in downloadStats.iteritems():
        print "   Download status: {}  count: {}".format(key, value)

