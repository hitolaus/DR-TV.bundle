#
# TODO:
# -
####################################################################################################

VIDEO_PREFIX = "/video/drtv"

ART = 'art-default.png'
ICON = 'icon-default.jpg'

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
    oc.add(DirectoryObject(key=Callback(HighlightList), title=L('Highlight Menu Title')))
    oc.add(DirectoryObject(key=Callback(SpotList), title=L('Spot Menu Title')))
    oc.add(DirectoryObject(key=Callback(NewestList), title=L('Newest Menu Title')))
    oc.add(DirectoryObject(key=Callback(LastChanceList), title=L('Last Chance Menu Title')))
    
    return oc
    
def MostViewedList():
    oc = ObjectContainer()
    return oc

def HighlightList():
    oc = ObjectContainer()
    return oc

def SpotList():
    oc = ObjectContainer()
    return oc

def NewestList():
    oc = ObjectContainer()
    return oc

def LastChanceList():
    oc = ObjectContainer()
    return oc

#####################################

def BrowseVideos(url):
    oc = ObjectContainer()
    
    for item in JSON.ObjectFromURL(url):
        oc.add(VideoClipObject(
            title = item['title'],
            summary = item['description'''],
            thumb = Resource.ContentsOfURLWithFallback('','icon-default.png'),
            url = ''))

    return oc