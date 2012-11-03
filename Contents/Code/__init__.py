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

LIVE_URL_BASE = 'http://lm.gss.dr.dk/V/V%sH.stream/Playlist.m3u8'

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

    oc.add(DirectoryObject(key=Callback(LiveTvList), title=L('Live TV Menu Title'), thumb = R('icon-tv.png')))
    oc.add(DirectoryObject(key=Callback(MostViewedList), title=L('Most Viewed Menu Title'), thumb = R('icon-popular.png')))
    oc.add(DirectoryObject(key=Callback(PremiereList), title=L('Premiere Menu Title'), thumb = R('icon-bookmark.png')))
    oc.add(DirectoryObject(key=Callback(NewestList), title=L('Newest Menu Title'), thumb = R('icon-flaged.png')))
    oc.add(DirectoryObject(key=Callback(LastChanceList), title=L('Last Chance Menu Title'), thumb = R('icon-last.png')))
    oc.add(DirectoryObject(key=Callback(AlphabeticallyList), title=L('A-Z Menu Title'), thumb = R('icon-menu.png')))
    
    return oc
    
def LiveTvList():
    oc = ObjectContainer()
    
    oc.add(VideoClipObject(
                    url = LIVE_URL_BASE % '01',
                    title = "DR1",
                    summary = "",
                    thumb = R('icon-channel-dr1.png')))
    oc.add(VideoClipObject(
                    url = LIVE_URL_BASE % '02',
                    title = "DR2",
                    summary = "",
                    thumb = R('icon-channel-dr2.png')))
    oc.add(VideoClipObject(
                    url = LIVE_URL_BASE % '06',
                    title = "DR HD",
                    summary = "",
                    thumb = R('icon-channel-drhd.png')))
    oc.add(VideoClipObject(
                    url = LIVE_URL_BASE % '05',
                    title = "DR Ramasjang",
                    summary = "",
                    thumb = R('icon-channel-ramasjang.png')))
    oc.add(VideoClipObject(
                    url = LIVE_URL_BASE % '04',
                    title = "DR K",
                    summary = "",
                    thumb = R('icon-channel-drk.png')))
    oc.add(VideoClipObject(
                    url = LIVE_URL_BASE % '03',
                    title = "DR Update",
                    summary = "",
                    thumb = R('icon-channel-update.png')))
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
    
    return VideoClipObject(
                title = item['title'],
                summary = item['formattedBroadcastTime'],
                thumb = Resource.ContentsOfURLWithFallback(thumb,R('icon-movie.png')),
                url = url)
    