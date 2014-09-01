#
# TODO:
# - Search http://www.dr.dk/tv/api/programmap?&searchType=contains&title=bonder%C3%B8ven&genre=&channelSlug=&includePreviews=true&orderByDate=false&limit=24&offset=0
####################################################################################################
from dateutil import parser

VIDEO_PREFIX = "/video/drtv"

ART = 'art-default.png'
ICON = 'icon-default.jpg'

PLATFORM='ipad'

API_MOBILE_BASE_URL = 'http://www.dr.dk/nu-mobil/api'
API_BASE_URL = 'http://www.dr.dk/nu/api'
API_META_URL = 'http://www.dr.dk/mu/programcard'

THUMB_WIDTH = '300'
THUMB_HEIGHT = '160'

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
    oc.add(DirectoryObject(key=Callback(GenresList), title=L('Genre Menu Title'), thumb = R('icon-starred.png')))
    oc.add(DirectoryObject(key=Callback(AlphabeticallyList), title=L('A-Z Menu Title'), thumb = R('icon-menu.png')))

    return oc


def GetLiveProgramDescription(slug):
    now = JSON.ObjectFromURL('http://www.dr.dk/TV/api/live/info/'+slug+'/json').get('Now')
    if not now:
        return {}

    return now

def LiveTvList():
    dr1 = GetLiveProgramDescription("dr1")
    dr2 = GetLiveProgramDescription("dr2")
    dr3 = GetLiveProgramDescription("dr3")
    ramasjang = GetLiveProgramDescription("dr-ramasjang")
    drk = GetLiveProgramDescription("dr-k")
    ultra = GetLiveProgramDescription("dr-ultra")

    oc = ObjectContainer()

    oc.add(VideoClipObject(
                    url = 'http://dr01-lh.akamaihd.net/i/dr01_0@147054/master.m3u8',
                    title = dr1.get('Title', 'DR1'),
                    summary = dr1.get('Description'),
                    thumb = R('icon-channel-dr1.png')))
    oc.add(VideoClipObject(
                    url = 'http://dr02-lh.akamaihd.net/i/dr02_0@147055/master.m3u8',
                    title = dr2.get('Title', 'DR2'),
                    summary = dr2.get('Description'),
                    thumb = R('icon-channel-dr2.png')))
    oc.add(VideoClipObject(
                    url = 'http://dr03-lh.akamaihd.net/i/dr03_0@147056/master.m3u8',
                    title = dr3.get('Title', 'DR3'),
                    summary = dr3.get('Description'),
                    thumb = R('icon-channel-dr3.png')))
    oc.add(VideoClipObject(
                    url = 'http://dr05-lh.akamaihd.net/i/dr05_0@147058/master.m3u8',
                    title = ramasjang.get('Title', 'DR Ramasjang'),
                    summary = ramasjang.get('Description'),
                    thumb = R('icon-channel-ramasjang.png')))
    oc.add(VideoClipObject(
                    url = 'http://dr04-lh.akamaihd.net/i/dr04_0@147057/master.m3u8',
                    title = drk.get('Title', 'DR K'),
                    summary = drk.get('Description'),
                    thumb = R('icon-channel-drk.png')))
    oc.add(VideoClipObject(
                    url = 'http://dr06-lh.akamaihd.net/i/dr06_0@147059/master.m3u8',
                    title = ultra.get('Title', 'DR Ultra'),
                    summary = ultra.get('Description'),
                    thumb = R('icon-channel-ultra.png')))
    return oc

def MostViewedList():
    return BrowseVideos(API_MOBILE_BASE_URL + '/mostviewed')

def HighlightList():
    return BrowseVideos(API_MOBILE_BASE_URL + '/highlights')

def NewestList():
    return BrowseVideos(API_MOBILE_BASE_URL + '/newest')

def PremiereList():
    return BrowseVideos(API_MOBILE_BASE_URL + '/premiere')

def BrowseGenre(url):
    oc = ObjectContainer()

    for program in JSON.ObjectFromURL(url)['ProgramSeries']:
        slug = program['ProgramSeriesSlug']

        title = program['Title']
        thumb = program['Image']
        url = API_MOBILE_BASE_URL +'/programserie?slug='+ slug

        oc.add(DirectoryObject(key = Callback(BrowseProgram, url = url),
                            title = title,
                            thumb = Resource.ContentsOfURLWithFallback(thumb,'icon-default.png')))

    return oc

def GenresList():
    oc = ObjectContainer()
    # http://www.dr.dk/nu-mobil/api/genres

    for genre in JSON.ObjectFromURL(API_MOBILE_BASE_URL+'/genres'):
        url = 'http://www.dr.dk/tv/api/programmap?&searchType=startswith&title=&genre='+genre.get('name')+'&channelSlug=&includePreviews=true&orderByDate=true&limit=50&offset=0'

        oc.add(DirectoryObject(key = Callback(BrowseGenre, url = url),
                                title = genre.get('name', 'Unknown')))

    return oc


# string.lowercase isn't supported
def getAllTheLetters(begin='A', end='Z'):
    letters = []

    beginNum = ord(begin)
    endNum = ord(end)
    for number in xrange(beginNum, endNum+1):
        letters.append(chr(number))

    return letters;


def AlphabeticallyList():
    oc = ObjectContainer()

    for i in getAllTheLetters():
        oc.add(DirectoryObject(key = Callback(BrowseAlphabet, letter = i), title = i))

    #Do a search - http://www.dr.dk/tv/api/programmap?&searchType=startswith&title=&genre=&channelSlug=&includePreviews=false&orderByDate=true&limit=24&offset=24

#     for item in HTML.ElementFromURL('http://www.dr.dk/nu-mobil/home/alphabetical').xpath('//li'):
#         #http://www.dr.dk/nu-mobil/api/programserie?label=
#         internal_link = item.xpath('.//a')[0].get('href')

#         slug = internal_link[internal_link.rindex("/")+1:]

#         thumb = API_BASE_URL+'/programseries/'+slug+'/images/'+THUMB_WIDTH+'x'+THUMB_HEIGHT+'.jpg'
#         url = API_MOBILE_BASE_URL +'/programserie?slug='+ slug

#         title = item.xpath('.//a/text()')[0]

#         title_pattern = Regex('(.*)\(([0-9]+)\)')
#         m = title_pattern.search(title)
#         episode_count = int(m.group(2))

#         title = m.group(1).strip()

# #        oc.add(DirectoryObject(key = Callback(BrowseProgram, url = url),
# #                            title = title,
# #                            thumb = Resource.ContentsOfURLWithFallback(thumb,'icon-default.png')))
#         oc.add(TVShowObject(key = Callback(BrowseProgram, url = url),
#                             rating_key = slug,
#                             title = title,
#                             episode_count = episode_count,
#                             thumb = Resource.ContentsOfURLWithFallback(thumb,'icon-default.png')))


    return oc

def BrowseAlphabet(letter):
    url = 'http://www.dr.dk/tv/api/programmap?&searchType=startswith&title=%s&genre=&channelSlug=&includePreviews=false&orderByDate=false&limit=100&offset=0' % letter

    oc = ObjectContainer()

    for item in JSON.ObjectFromURL(url)['ProgramSeries']:

        url = API_MOBILE_BASE_URL +'/programserie?slug='+ item['ProgramSeriesSlug']

        #oc.add(BrowseProgram(url))

        oc.add(DirectoryObject(key=Callback(BrowseProgram, url=url), title=item['Title'], thumb=item['Image']))

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


# {
#   u'programSerieSlug': u'den-store-julebagedyst-2013',
#   u'broadcastTime': u'2013-12-25T20:00:00+01:00',
#   u'formattedBroadcastTime': u'25. Dec. 2013',
#   u'id': u'den-store-julebagedyst-2013',
#   u'title': u'Den store julebagedyst 2013'
#}
def GetVideoClip(item):

    thumb = 'http://asset.dr.dk/drdkimagescale/imagescale.drxml?server=www.dr.dk&w='+THUMB_WIDTH+'&h='+THUMB_HEIGHT+'&file=/mu/programcard/imageuri/' + item['id'] + '&scaleAfter=crop&contenttype=jpg'
    url = API_MOBILE_BASE_URL+'/videos/'+item['id']+'?platform='+PLATFORM

    meta = JSON.ObjectFromURL(API_META_URL+'/'+item['id'])

    # {
    #   u'TotalSize': 1,
    #   u'ResultSize': 1,
    #   u'Data': [
    #       {
    #           u'SiteUrl': None,
    #           u'Title': u'Dokumania: Pirate Bay indefra',
    #           u'LastModified': u'2014-01-04T21:00:51.781Z',
    #           u'ProductionNumber': u'00921280060',
    #           u'Site': u'radio-tv',
    #           u'Broadcasts': [
    #               {
    #                   u'ProductionCountry': u'DANMARK',
    #                   u'TransmissionOid': 195094417812,
    #                   u'Description': u'Det er dagen f\xf8r retssagen begynder. Fredrik pakker en computer i en rusten gammel Volvo. Sammen med hans Pirate Bay-medstiftere st\xe5r han ansigt til ansigt med et erstatningskrav fra Hollywood p\xe5 72 millioner kroner i en sag om kr\xe6nkelse af ophavsret. Fredrik er p\xe5 vej hen for at installere en ny computer i den hemmelige serverhal. Det er her verdens st\xf8rste fildelingsside er gemt. \nDa hacker-vidunderbarnet Gottfrid, internetaktivisten Peter og den fordrukne webn\xf8rd Fredrik findes skyldige i retssagen bliver de konfronteret med virkeligheden i form af et liv offline - v\xe6k fra tastaturet. Men dybt nede i de m\xf8rke datacentre forts\xe6tter skjulte computere stille med at kopiere filer.',
    #                   u'Title': u'Dokumania: Pirate Bay indefra',
    #                   u'AnnouncedEndTime': u'2013-02-26T21:30:00Z',
    #                   u'FirstPartOid': 195094418813,
    #                   u'Key': u'dr.dk/mas/whatson/195094418813@dr.dk/mas/whatson/channel/DR2',
    #                   u'BroadcastDate': u'2013-02-26T00:00:00Z',
    #                   u'ProductionYear': 2012,
    #                   u'StartTime': u'2013-02-26T19:59:13.32Z',
    #                   u'VideoWidescreen': True,
    #                   u'AnnouncedStartTime': u'2013-02-26T20:00:00Z',
    #                   u'WhatsOnUri': u'dr.dk/mas/whatson/195094418813',
    #                   u'EndTime': u'2013-02-26T21:29:55Z',
    #                   u'IsRerun': False,
    #                   u'Channel': u'dr.dk/mas/whatson/channel/DR2',
    #                   u'Punchline': u'Dansk dokumentar fra 2013.'
    #               },
    #               {
    #                   u'ProductionCountry': u'DANMARK',
    #                   u'TransmissionOid': 199189366812,
    #                   u'Description': u'Det er dagen f\xf8r retssagen begynder. Fredrik pakker en computer i en rusten gammel Volvo. Sammen med hans Pirate Bay-medstiftere st\xe5r han ansigt til ansigt med et erstatningskrav fra Hollywood p\xe5 72 millioner kroner i en sag om kr\xe6nkelse af ophavsret. Fredrik er p\xe5 vej hen for at installere en ny computer i den hemmelige serverhal. Det er her verdens st\xf8rste fildelingsside er gemt. \nDa hacker-vidunderbarnet Gottfrid, internetaktivisten Peter og den fordrukne webn\xf8rd Fredrik findes skyldige i retssagen bliver de konfronteret med virkeligheden i form af et liv offline - v\xe6k fra tastaturet. Men dybt nede i de m\xf8rke datacentre forts\xe6tter skjulte computere stille med at kopiere filer.',
    #                   u'Title': u'DR3 Dok: Pirate Bay indefra',
    #                   u'AnnouncedEndTime': u'2013-03-25T20:25:00Z',
    #                   u'FirstPartOid': 199189367813,
    #                   u'Key': u'dr.dk/mas/whatson/199189367813@dr.dk/mas/whatson/channel/DR3',
    #                   u'BroadcastDate': u'2013-03-25T00:00:00Z',
    #                   u'VideoHD': True,
    #                   u'ProductionYear': 2012,
    #                   u'StartTime': u'2013-03-25T18:58:38.24Z',
    #                   u'VideoWidescreen': True,
    #                   u'AnnouncedStartTime': u'2013-03-25T19:00:00Z',
    #                   u'WhatsOnUri': u'dr.dk/mas/whatson/199189367813',
    #                   u'EndTime': u'2013-03-25T20:22:58.64Z',
    #                   u'IsRerun': False,
    #                   u'Channel': u'dr.dk/mas/whatson/channel/DR3',
    #                   u'Punchline': u'Dansk dokumentar fra 2013.'
    #               },
    #               {
    #                   u'ProductionCountry': u'DANMARK',
    #                   u'TransmissionOid': 193370133812,
    #                   u'Description': u'Det er dagen f\xf8r retssagen begynder. Fredrik pakker en computer i en rusten gammel Volvo. Sammen med hans Pirate Bay-medstiftere st\xe5r han ansigt til ansigt med et erstatningskrav fra Hollywood p\xe5 72 millioner kroner i en sag om kr\xe6nkelse af ophavsret. Fredrik er p\xe5 vej hen for at installere en ny computer i den hemmelige serverhal. Det er her verdens st\xf8rste fildelingsside er gemt. \nDa hacker-vidunderbarnet Gottfrid, internetaktivisten Peter og den fordrukne webn\xf8rd Fredrik findes skyldige i retssagen bliver de konfronteret med virkeligheden i form af et liv offline - v\xe6k fra tastaturet. Men dybt nede i de m\xf8rke datacentre forts\xe6tter skjulte computere stille med at kopiere filer.',
    #                   u'Title': u'DR3 Dok: Pirate Bay indefra',
    #                   u'AnnouncedEndTime': u'2013-03-30T14:00:00Z',
    #                   u'FirstPartOid': 193370134813,
    #                   u'Key': u'dr.dk/mas/whatson/193370134813@dr.dk/mas/whatson/channel/DR3',
    #                   u'BroadcastDate': u'2013-03-30T00:00:00Z',
    #                   u'VideoHD': True, u'ProductionYear': 2012,
    #                   u'StartTime': u'2013-03-30T12:37:08Z',
    #                   u'VideoWidescreen': True,
    #                   u'AnnouncedStartTime': u'2013-03-30T12:35:00Z',
    #                   u'WhatsOnUri': u'dr.dk/mas/whatson/193370134813',
    #                   u'EndTime': u'2013-03-30T14:00:06.76Z',
    #                   u'IsRerun': False,
    #                   u'Channel': u'dr.dk/mas/whatson/channel/DR3',
    #                   u'Punchline': u'Dansk dokumentar fra 2013.'
    #               },
    #               {
    #                   u'ProductionCountry': u'DANMARK',
    #                   u'TransmissionOid': 201217098812,
    #                   u'Description': u'Det er dagen f\xf8r retssagen begynder. Fredrik pakker en computer i en rusten gammel Volvo. Sammen med hans Pirate Bay-medstiftere st\xe5r han ansigt til ansigt med et erstatningskrav fra Hollywood p\xe5 72 millioner kroner i en sag om kr\xe6nkelse af ophavsret. Fredrik er p\xe5 vej hen for at installere en ny computer i den hemmelige serverhal. Det er her verdens st\xf8rste fildelingsside er gemt. \nDa hacker-vidunderbarnet Gottfrid, internetaktivisten Peter og den fordrukne webn\xf8rd Fredrik findes skyldige i retssagen bliver de konfronteret med virkeligheden i form af et liv offline - v\xe6k fra tastaturet. Men dybt nede i de m\xf8rke datacentre forts\xe6tter skjulte computere stille med at kopiere filer.',
    #                   u'Title': u'DR3 Dok: Pirate Bay indefra',
    #                   u'AnnouncedEndTime': u'2013-04-04T00:35:00Z',
    #                   u'FirstPartOid': 201217099813, u'Key':
    #                   u'dr.dk/mas/whatson/201217099813@dr.dk/mas/whatson/channel/DR3',
    #                   u'BroadcastDate': u'2013-04-03T00:00:00Z',
    #                   u'VideoHD': True,
    #                   u'ProductionYear': 2012,
    #                   u'StartTime': u'2013-04-03T23:14:00.28Z',
    #                   u'VideoWidescreen': True,
    #                   u'AnnouncedStartTime': u'2013-04-03T23:15:00Z',
    #                   u'WhatsOnUri': u'dr.dk/mas/whatson/201217099813',
    #                   u'EndTime': u'2013-04-04T00:36:44.04Z',
    #                   u'IsRerun': False,
    #                   u'Channel': u'dr.dk/mas/whatson/channel/DR3',
    #                   u'Punchline': u'Dansk dokumentar fra 2013.'
    #               },
    #               {
    #                   u'ProductionCountry': u'DANMARK',
    #                   u'TransmissionOid': 201940946812,
    #                   u'Description': u'Det er dagen f\xf8r retssagen begynder. Fredrik pakker en computer i en rusten gammel Volvo. Sammen med hans Pirate Bay-medstiftere st\xe5r han ansigt til ansigt med et erstatningskrav fra Hollywood p\xe5 72 millioner kroner i en sag om kr\xe6nkelse af ophavsret. Fredrik er p\xe5 vej hen for at installere en ny computer i den hemmelige serverhal. Det er her verdens st\xf8rste fildelingsside er gemt. \nDa hacker-vidunderbarnet Gottfrid, internetaktivisten Peter og den fordrukne webn\xf8rd Fredrik findes skyldige i retssagen bliver de konfronteret med virkeligheden i form af et liv offline - v\xe6k fra tastaturet. Men dybt nede i de m\xf8rke datacentre forts\xe6tter skjulte computere stille med at kopiere filer.',
    #                   u'Title': u'DR3 Dok: Pirate Bay indefra',
    #                   u'AnnouncedEndTime': u'2013-04-11T15:45:00Z',
    #                   u'FirstPartOid': 201940947813,
    #                   u'Key': u'dr.dk/mas/whatson/201940947813@dr.dk/mas/whatson/channel/DR3',
    #                   u'BroadcastDate': u'2013-04-11T00:00:00Z',
    #                   u'VideoHD': True,
    #                   u'ProductionYear': 2012,
    #                   u'StartTime': u'2013-04-11T14:25:15Z',
    #                   u'VideoWidescreen': True,
    #                   u'AnnouncedStartTime': u'2013-04-11T14:25:00Z',
    #                   u'WhatsOnUri': u'dr.dk/mas/whatson/201940947813',
    #                   u'EndTime': u'2013-04-11T15:48:28.76Z',
    #                   u'IsRerun': False,
    #                   u'Channel': u'dr.dk/mas/whatson/channel/DR3',
    #                   u'Punchline': u'Dansk dokumentar fra 2013.'
    #               },
    #               {
    #                   u'ProductionCountry': u'DANMARK',
    #                   u'TransmissionOid': 234677919812,
    #                   u'Description': u'Det er dagen f\xf8r retssagen begynder. Fredrik pakker en computer i en rusten gammel Volvo. Sammen med hans Pirate Bay-medstiftere st\xe5r han ansigt til ansigt med et erstatningskrav fra Hollywood p\xe5 72 millioner kroner i en sag om kr\xe6nkelse af ophavsret. Fredrik er p\xe5 vej hen for at installere en ny computer i den hemmelige serverhal. Det er her verdens st\xf8rste fildelingsside er gemt. \nDa hacker-vidunderbarnet Gottfrid, internetaktivisten Peter og den fordrukne webn\xf8rd Fredrik findes skyldige i retssagen bliver de konfronteret med virkeligheden i form af et liv offline - v\xe6k fra tastaturet. Men dybt nede i de m\xf8rke datacentre forts\xe6tter skjulte computere stille med at kopiere filer.',
    #                   u'Title': u'Pirate Bay indefra',
    #                   u'AnnouncedEndTime': u'2013-12-31T12:40:00Z',
    #                   u'FirstPartOid': 234677920813,
    #                   u'Key': u'dr.dk/mas/whatson/234677920813@dr.dk/mas/whatson/channel/DR3',
    #                   u'_ProductionTag': u'OV - on demand video (WEBCMS)',
    #                   u'BroadcastDate': u'2013-12-31T00:00:00Z',
    #                   u'VideoHD': True, u'ProductionYear': 2012,
    #                   u'Channel': u'dr.dk/mas/whatson/channel/DR3',
    #                   u'StartTime': u'2013-12-31T11:17:08.04Z',
    #                   u'VideoWidescreen': True,
    #                   u'AnnouncedStartTime': u'2013-12-31T11:15:00Z',
    #                   u'WhatsOnUri': u'dr.dk/mas/whatson/234677920813',
    #                   u'EndTime': u'2013-12-31T12:40:26.64Z',
    #                   u'IsRerun': False,
    #                   u'_SubtitleType': u'FOREIGN',
    #                   u'Punchline': u'Dansk dokumentar fra 2013.'
    #               }
    #           ],
    #           u'Version': 52,
    #           u'CreatedTime': u'2013-02-13T05:32:50.043Z',
    #           u'GenreCode': u'2:0',
    #           u'_Gallery': u'/Resources/dr.dk/NETTV/DR3/',
    #           u'Description': u'Det er dagen f\xf8r retssagen begynder. Fredrik pakker en computer i en rusten gammel Volvo. Sammen med hans Pirate Bay-medstiftere st\xe5r han ansigt til ansigt med et erstatningskrav fra Hollywood p\xe5 72 millioner kroner i en sag om kr\xe6nkelse af ophavsret. Fredrik er p\xe5 vej hen for at installere en ny computer i den hemmelige serverhal. Det er her verdens st\xf8rste fildelingsside er gemt. \nDa hacker-vidunderbarnet Gottfrid, internetaktivisten Peter og den fordrukne webn\xf8rd Fredrik findes skyldige i retssagen bliver de konfronteret med virkeligheden i form af et liv offline - v\xe6k fra tastaturet. Men dybt nede i de m\xf8rke datacentre forts\xe6tter skjulte computere stille med at kopiere filer.', u'OnlineGenreText': u'Dokumentar', u'PrimaryBroadcastWhatsOnUri': u'dr.dk/mas/whatson/234677920813', u'Relations': [{u'BundleType': u'Series', u'Kind': u'MemberOf', u'Urn': u'urn:dr:mu:bundle:4f3b98a2860d9a33ccfdd571', u'Slug': u'dokumania'}], u'ProductionYear': 2012, u'_PostingGuid': u'{e7e55b32-300a-4504-a864-5e107b9cddc4}', u'ChannelType': u'TV', u'PrimaryAssetStartPublish': u'2013-12-31T11:17:05Z', u'Slug': u'dokumania-pirate-bay-indefra', u'ProductionCountry': u'DANMARK', u'EndPublish': u'9999-12-31T22:59:59Z', u'_ResourceId': 1667922, u'Assets': [{u'Kind': u'VideoResource', u'StartPublish': u'2013-12-31T11:17:05Z', u'EndPublish': u'2014-01-30T11:17:05Z', u'Uri': u'http://www.dr.dk/mu/bar/52c2a60ca11f9d19dccc9234', u'RestrictedToDenmark': True, u'DurationInMilliseconds': 4917000, u'Trashed': False}, {u'Kind': u'Image', u'ContentType': u'image/jpeg', u'Name': u'piratebay.jpg', u'StartPublish': u'2013-12-31T16:45:01.233Z', u'EndPublish': u'9999-12-31T22:59:59Z', u'Uri': u'http://www.dr.dk/mu/bar/52c2f4936187a21b604b0103', u'Id': u'hpvdzpwx', u'Size': 161586}, {u'Kind': u'Image', u'ContentType': u'image/jpeg', u'Name': u'pirate Bay indefra.jpg', u'StartPublish': u'2013-02-27T08:57:26.999Z', u'EndPublish': u'9999-12-31T22:59:59Z', u'Uri': u'http://www.dr.dk/mu/Bar/512dca82860d9a3104d68d4a', u'Id': u'hdo93wjc', u'Trashed': False, u'Size': 75644}, {u'StartPublish': u'0001-01-01T00:00:00Z', u'Kind': u'Image', u'EndPublish': u'9999-12-31T22:59:59.999Z', u'Uri': u'http://www.dr.dk/mu/bar/52c2a611a11f9d19dccc9235', u'Trashed': False}], u'StartPublish': u'0001-01-01T00:00:00Z', u'Urn': u'urn:dr:mu:programcard:511b2582860d9a17f019f795',
    #           u'ModifiedBy': u'NET\\MPAG',
    #           u'Dirty': True,
    #           u'PrimaryBroadcastStartTime': u'2013-12-31T11:15:00Z',
    #           u'PrimaryAssetUri': u'http://www.dr.dk/mu/bar/52c2a60ca11f9d19dccc9234',
    #           u'PrimaryAssetEndPublish': u'2014-01-30T11:17:05Z',
    #           u'PrimaryBroadcastDirty': False,
    #           u'Subtitle': u'Dansk dokumentar fra 2013.',
    #           u'RtmpHost': u'rtmp://vod-prio3.gss.dr.dk',
    #           u'PrimaryChannel': u'dr.dk/mas/whatson/channel/DR2',
    #           u'PrimaryBroadcastChannel': u'dr.dk/mas/whatson/channel/DR3',
    #           u'PresentationUri': u'http://www.dr.dk/tv/se/dokumania/dokumania-pirate-bay-indefra',
    #           u'CardType': u'Program',
    #           u'PrimaryAssetKind': u'VideoResource',
    #           u'CreatedBy': u'Application@MU01',
    #           u'GenreText': u'Dokumentar'
    #       }
    #   ],
    #   u'ResultGenerated': u'2014-01-04T23:24:02.2649194Z', u'ResultProcessingTime': 1}

    description = meta['Data'][0]['Description']
    aired = parser.parse(meta['Data'][0].get('PrimaryBroadcastStartTime', '1970-01-01T01:00:00Z'))

    return VideoClipObject(
                title=item['title'],
                summary=description,
                originally_available_at=aired,
                thumb=Resource.ContentsOfURLWithFallback(thumb,R('icon-movie.png')),
                url=url)

