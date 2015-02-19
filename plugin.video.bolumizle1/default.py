import sys
import xbmcgui
import xbmcplugin
import urllib2
import urllib
import re
from bs4 import BeautifulSoup
#import codecs
#import sys
#streamWriter = codecs.lookup('utf-8')[-1]
#sys.stdout = streamWriter(sys.stdout)

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'movies')


def CATEGORIES():
	addDir('Serien','http://www.bolumizle1.com/',1,'http://www.bolumizle1.com/wp-content/themes/keremiya/logo/logo.png')
                       
def INDEX(p_url):
	print('INDEX url '+p_url)
	req = urllib2.Request(p_url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
#	link=response.read()
#	link=response.read().decode('utf-8', 'ignore')
	link=response.read().decode('ascii','ignore')
#        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
	response.close()
	soup = BeautifulSoup(link, from_encoding='latin5')
	print(soup.original_encoding)
#	convertEntities=BeautifulSoup.HTML_ENTITIES
#	print(soup.prettify(encoding="latin5"))
#		print(soup.title.name)
#	print(soup.prettify())
#	serien = [i.findAll('li') for i in soup('div', {'class': 'sidebar-right'})]
	serien = soup.findAll("li", {"class" : re.compile('cat-item.*')})
	for i in serien:
		all = i.find("a")
#		print(all)
		print('INDEX name '+all.string)
		print('INDEX href '+all.attrs['href'])
		addDir(all.string,all.attrs['href'],2,'next.png')
#	for link1 in soup.find_all('a'):
#		print(link1.get('href'))

def SUB_INDEX(p_url):
	print('SUB_INDEX url '+p_url)
	req = urllib2.Request(p_url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
#	link=response.read()
#	link=response.read().decode('utf-8', 'ignore')
	link=response.read().decode('ascii','ignore')
#        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
	response.close()
	soup = BeautifulSoup(link, from_encoding='latin5')
#	print(soup.original_encoding)
#	convertEntities=BeautifulSoup.HTML_ENTITIES
#	print(soup.prettify(encoding="latin5"))
#		print(soup.title.name)
#	print(soup.prettify())
#	serien = [i.findAll('li') for i in soup('div', {'class': 'sidebar-right'})]
	serien = soup.findAll("div", {"class" : "moviefilm"})
	for i in serien:
		all = i.find("a")
		img = i.find("img")
		print('SUB_INDEX href '+all.attrs['href'])
		print('SUB_INDEX name '+img.attrs['alt'])
		print('SUB_INDEX img '+img.attrs['src'])	
		addDir(img.attrs['alt'],all.attrs['href'],3,img.attrs['src'])
#	for link1 in soup.find_all('a'):
#		print(link1.get('href'))

def start_video(url):
		#url = 'http://www.bolumizle1.com/seref-meselesi-11-bolum-hd-izle.html'
		#url = 'http://www.bolumizle1.com/aci-hayat-57-bolum-izle.html'
#		url = 'http://www.bolumizle1.com/beni-boyle-sev-82-bolum-izle.html'
		print(url)
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		# print(link)
		soup = BeautifulSoup(link)
		#mydivs = soup.findAll("div", { "class" : "filmicerik" })
		#for div in mydivs: 
		#	gm = BeautifulSoup(div)
		#	myiframe=getmovie.iFrame
		#	for ifr in myiframe:
		#		print ifr


		iframes = [i.find('iframe') for i in soup('div', {'class': 'filmicerik'})]
		for i in iframes:
			print(i.attrs['src'])
			if (i.attrs['src'].find('netd.com')	> 0):
				print('netd.com')
				req = urllib2.Request(i.attrs['src'])
				req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
				response = urllib2.urlopen(req)
				link=response.read()
			#	link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g").replace('\xC5',"S").replace('\x9E',"S")
				response.close()
				print(link)
				iframe = BeautifulSoup(link)
				itemurl = iframe.find("meta", {"itemprop":"contentURL"})
				print('http://media.netd.com.tr'+itemurl['content'])
				itemimage = iframe.find("meta", {"itemprop":"thumbnailUrl"})
			#	print(itemimage['content'])	
				li = xbmcgui.ListItem('Start', iconImage=itemimage['content'])
				xbmcplugin.addDirectoryItem(handle=addon_handle, url='http://media.netd.com.tr'+itemurl['content'], listitem=li)	
			elif (i.attrs['src'].find('youtube') > 0):
				print('youtube.com '+i.attrs['src'])
				# //www.youtube.com/embed/mZ1nL3va2nU
				video_id = i.attrs['src'].replace('//','').split('/')[2]
				playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id
				
				print(playback_url)
				item = xbmcgui.ListItem(path=playback_url)
				xbmcplugin.setResolvedUrl(addon_handle, True, item)
		#		xbmcplugin.addDirectoryItem(handle=addon_handle, url=playback_url, listitem=item)
				icon = "DefaultVideo.png"
				addDir('Part 1',url,3,icon)
				parts = soup.findAll("div", {"class" : "keremiya_part"})
				for part in parts:
					j = 1
					allp = part.findAll("a")
					for parturl in allp:
						j = j + 1
						addDir('Part '+str(j),parturl["href"],3,icon)				
				
				xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(playback_url)

			elif (i.attrs['src'].find('dailymotion.com') > 0):
				print('dailymotion.com '+i.attrs['src'])
				# http://www.dailymotion.com/embed/video/x2egjbg?autoplay=0&logo=1&hideInfos=0&start=0&syndication=134357&foreground=&highlight=&background=
				icon = "DefaultVideo.png"				
				
				video_id = i.attrs['src'].replace('//','').split('/')[3].split('?')[0]
				playback_url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % video_id	
				print('dailymotion '+playback_url)
				addDir('Part 1',url,3,icon)
				parts = soup.findAll("div", {"class" : "keremiya_part"})
				for part in parts:
					j = 1
					allp = part.findAll("a")
					for parturl in allp:
						j = j + 1
						addDir('Part '+str(j),parturl["href"],3,icon)
				
				
				playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
				playlist.clear()
				listitem = xbmcgui.ListItem( 'Start me', iconImage=icon, thumbnailImage="")
				listitem.setInfo( "video", { "Title": 'Start me' } )
				playlist.add( playback_url, listitem )
				xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play( playlist )
#				SUB_INDEX(url)
				#				item = xbmcgui.ListItem('Starte Video', iconImage=ICON)
#				item = xbmcgui.ListItem('Starte Video', path=playback_url)
#				xbmcplugin.setResolvedUrl(addon_handle, True, item)
#				xbmcplugin.addDirectoryItem(handle=addon_handle, url=playback_url, listitem=item)
#				xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(playback_url)
				xbmcplugin.endOfDirectory(addon_handle)
				
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

		
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
	print ""
	CATEGORIES()
       
elif mode==1:
	print ""+url
	INDEX(url)
        
elif mode==2:
	print ""+url
	SUB_INDEX(url)
elif mode==3:
	print ""+url
	start_video(url)	

#INDEX('http://www.bolumizle1.com/')	
xbmcplugin.endOfDirectory(addon_handle)