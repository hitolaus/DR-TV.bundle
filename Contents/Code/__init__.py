#
# TODO:
# -
####################################################################################################

VIDEO_PREFIX = "/video/drtv"

ART = 'art-default.png'
ICON = 'icon-default.jpg'

PLATFORM='ipad'

API_MOBILE_BASE_URL = 'http://www.dr.dk/nu-mobil/api'
API_BASE_URL = 'http://www.dr.dk/nu/api'

THUMB_WIDTH = '300'
THUMB_HEIGHT = '120'

# This function is initially called by the PMS framework to initialize the plugin. This includes
# setting up the Plugin static instance along with the displayed artwork.
def Start():

    Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
    Plugin.AddViewGroup('List', viewMode = 'List', mediaType = 'items')

    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = L('Title')
    ObjectContainer.view_group = 'List'

    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)
    VideoClipObject.thumb = R(ICON)
    VideoClipObject.art = R(ART)

# This main function will setup the displayed items.
@handler(VIDEO_PREFIX, L('Title'), ICON, ART)
def MainMenu():

    oc = ObjectContainer()

    # TODO: Live channels
    oc.add(DirectoryObject(key=Callback(MostViewedList), title=L('Most Viewed Menu Title')))
#    oc.add(DirectoryObject(key=Callback(HighlightList), title=L('Highlight Menu Title')))
    oc.add(DirectoryObject(key=Callback(PremiereList), title=L('Premiere Menu Title')))
    oc.add(DirectoryObject(key=Callback(NewestList), title=L('Newest Menu Title')))
    oc.add(DirectoryObject(key=Callback(LastChanceList), title=L('Last Chance Menu Title')))
    oc.add(DirectoryObject(key=Callback(AlphabeticallyList), title=L('A-Z Menu Title')))
    
    return oc
    
def MostViewedList():
    return BrowseVideos(API_MOBILE_BASE_URL + '/mostviewed')

def HighlightList():
    return BrowseVideos(API_MOBILE_BASE_URL + '/highlights')

def NewestList():
    return BrowseVideos(API_MOBILE_BASE_URL + '/newest')

def LastChanceList():
    return BrowseVideos(API_MOBILE_BASE_URL + '/lastchance')

def PremiereList():
    return BrowseVideos(API_MOBILE_BASE_URL + '/premiere')

def AlphabeticallyList():
    oc = ObjectContainer()
    
    for item in HTML.ElementFromURL('http://www.dr.dk/nu-mobil/home/alphabetical').xpath('//li'):
        #http://www.dr.dk/nu-mobil/api/programserie?label=
        internal_link = item.xpath('.//a')[0].get('href')
        
        slug = internal_link[internal_link.rindex("/")+1:]
        
        thumb = API_BASE_URL+'/programseries/'+slug+'/images/'+THUMB_WIDTH+'x'+THUMB_HEIGHT+'.jpg'
        url = API_MOBILE_BASE_URL +'/programserie?slug='+ slug

        title = item.xpath('.//a/text()')[0]
        
        oc.add(DirectoryObject(key = Callback(BrowseProgram, url = url),
                            title = title,
                            thumb = Resource.ContentsOfURLWithFallback(thumb,'icon-default.png')))
    return oc

#####################################

def BrowseProgram(url):
    oc = ObjectContainer()
    
    for item in JSON.ObjectFromURL(url)['videos']:
        oc.add(GetVideoClip(item))
        
    return oc

def BrowseVideos(url):
    oc = ObjectContainer()
    
    for item in JSON.ObjectFromURL(url):
        oc.add(GetVideoClip(item))

    return oc

def GetVideoClip(item):
    #thumb = API_BASE_URL+'/programseries/'+item['programSerieSlug']+'/images/'+THUMB_WIDTH+'x'+THUMB_HEIGHT+'.jpg'
    thumb = 'http://www.dr.dk/nu-mobil/nuapi/videos/'+item['id']+'/images/'+THUMB_WIDTH+'x'+THUMB_HEIGHT+'.jpg'
    url = API_MOBILE_BASE_URL+'/videos/'+item['id']+'?platform='+PLATFORM
    
    Log(thumb)
    
    return VideoClipObject(
                title = item['title'],
                summary = item['formattedBroadcastTime'],
                thumb = Resource.ContentsOfURLWithFallback(thumb,'icon-default.png'),
                url = url)
