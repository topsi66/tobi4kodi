import sys
import xbmcgui
import xbmcplugin
import urllib2
import urllib
import re
import urlresolver
import json
from bs4 import BeautifulSoup
from cookielib import CookieJar
#import codecs
#import sys
#streamWriter = codecs.lookup('utf-8')[-1]
#sys.stdout = streamWriter(sys.stdout)

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'movies')


def CATEGORIES():
	addDir('Serien','http://www.bolumizle1.com/tum-diziler',1,'http://www.bolumizle1.com/wp-content/themes/keremiya/logo/logo.png')
                       
def INDEX(p_url):
	print('INDEX url '+p_url)
	req = urllib2.Request(p_url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read().decode('ascii','ignore')
	response.close()
	soup = BeautifulSoup(link, from_encoding='latin5')
	print(soup.original_encoding)
	
	serien = soup.findAll("td", {"class" : "blocklu"})
	for i in serien:
		all = i.find("a")
		img = all.find("span")
		addDir(img.string,all.attrs['href'],2,'default')

def SUB_INDEX(p_url):
	print('SUB_INDEX url '+p_url)
	req = urllib2.Request(p_url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read().decode('ascii','ignore')
	response.close()
	soup = BeautifulSoup(link, from_encoding='latin5')
	serien = soup.findAll("div", {"class" : "padder-v"})
	for i in serien:
		all = i.find("a")
#		print('SUB_INDEX href '+all.attrs['href'])
#		print('SUB_INDEX name '+all.attrs['title'])
#		print('SUB_INDEX img '+img.attrs['src'])	
		addDir(all.attrs['title'],all.attrs['href'],3,'default')


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


		if (link.count('<div id="tekpartli"') > 0):
			iframes = [i.find('iframe') for i in soup('div', {'id': 'tekpartli'})]
		else:
			iframes = [i.find('iframe') for i in soup('div', {'id': 'konumuz'})]
#		iframes = [i.find('iframe') for i in soup('div', {'id': 'konumuz'})]
		for i in iframes:
			print('starte video src '+i.attrs['src'])
			if (i.attrs['src'].find('netd.com')	> 0):
				print('netd.com')
				req = urllib2.Request(i.attrs['src'])
				req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
				response = urllib2.urlopen(req)
				link=response.read()
			#	link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g").replace('\xC5',"S").replace('\x9E',"S")
				response.close()
				iframe = BeautifulSoup(link)		
#				print (iframe)
				scripturl = iframe.body.script.string.replace('window.top.location.href = "','').replace('";','')
#				print (scripturl)
				
				req = urllib2.Request(scripturl)
				req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
				response = urllib2.urlopen(req)
				link=response.read()
			#	link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g").replace('\xC5',"S").replace('\x9E',"S")
				response.close()
				iframe = BeautifulSoup(link)		
				
				itemurl = iframe.find("meta", {"itemprop":"contentURL"})
				print('http://media.netd.com.tr'+itemurl['content'])
				itemimage = iframe.find("meta", {"itemprop":"thumbnailUrl"})
			#	print(itemimage['content'])	
				li = xbmcgui.ListItem('Start', iconImage=itemimage['content'])
				xbmcplugin.addDirectoryItem(handle=addon_handle, url='http://media.netd.com.tr'+itemurl['content'], listitem=li)
			elif (i.attrs['src'].find('vid.ag')	> 0):
				print('vid.ag')
				req = urllib2.Request(i.attrs['src'])
				req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
				response = urllib2.urlopen(req)
				link=response.read().decode('ascii','ignore')
				response.close()
				for inter in range(1,50):
					if (link.split("|")[inter] == "vid"):
						vid_id = link.split("|")[inter+2]
					if (link.split("|")[inter] == "fviews"):
						vid_hash = link.split("|")[inter-1]
						break
				print("vid_id="+vid_id+" vid_hash="+vid_hash)						
				li = xbmcgui.ListItem('Start', iconImage='default')
				xbmcplugin.addDirectoryItem(handle=addon_handle, url='http://vid.ag/'+vid_hash+".m3u8", listitem=li)				
			elif (i.attrs['src'].find('vk.com') > 0):
			# url360=http://cs634202v6.vk.me/u294779102/videos/47fab64a09.360.mp4?extra=utKtnOoq241Iag5Cv7QEQsfzgfJ4gUR9NpJhb48_MKv9jmBmPgIPvg7ywAOEy-VTsvKd5fwEc7d3dNRYQwy5R_jT_HCSTZEs8s8xges83UMFJeBy9N4v8ZqmLSyF31fh2g&amp
				req = urllib2.Request('http:'+i.attrs['src'])
				req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
				response = urllib2.urlopen(req)
				link=response.read()
				response.close()
				posxlink=link.find('url360=')
#				posxlink=link.find('url240=')
				print(posxlink)
				posylink=link.find('?',posxlink)
				print(posylink)
				print (link[posxlink+7:posylink].replace('&amp',''))
				
				li = xbmcgui.ListItem('Start', iconImage='icon')
				xbmcplugin.addDirectoryItem(handle=addon_handle, url=link[posxlink+7:posylink].replace('&amp',''), listitem=li)
			elif (i.attrs['src'].find('mail.ru') > 0):
				# 'http://videoapi.my.mail.ru/videos/embed/mail/acundizi/_myvideo/1555.html'
				json_url = i.attrs['src'].replace('.html','.json').replace('/embed','')
				cj = CookieJar()
				opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
				opener.addheaders= [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'),('Accept-encoding', 'gzip'),('Referer', 'http://videoapi.my.mail.ru/videos/embed/mail/acundizi/_myvideo/1575.html')]
				urllib2.install_opener(opener)
				req = urllib2.Request(json_url)
				file_e =urllib2.urlopen(req)
				cookies={}
				for cookie in cj:
					if "mail.ru" in cookie.domain:
						cookies[cookie.name]=cookie.value	
				req = urllib2.Request(json_url)
				req.add_header('Cookie', 'video_key='+cookies['video_key'])
				file_e =urllib2.urlopen(req)
				json_file = unicode(file_e.read())
				jobj = json.loads(json_file)
				movie_url = urllib.unquote(jobj['videos'][0]['url'])+"|Cookie="+"video_key="+cookies['video_key']
				print ('URL mail.ru: '+movie_url)
				li = xbmcgui.ListItem('Start', iconImage="DefaultVideo.png")
				xbmcplugin.addDirectoryItem(handle=addon_handle, url=movie_url, listitem=li)
				xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(movie_url)
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
				parts = soup.findAll("ul", {"class" : "pagination pagination-md yuvarla"})
				print(parts)
				for part in parts:
					j = 1
					allp = part.findAll("a")
					for parturl in allp:
						if (parturl["href"]<>""):
							addDir(parturl.string,parturl["href"],3,icon)
						else:
							addDir(parturl.string,url,3,icon)			
				
				xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(playback_url)

			elif (i.attrs['src'].find('dailymotion.com') > 0):
				print('dailymotion.com '+i.attrs['src'])
				# http://www.dailymotion.com/embed/video/x2egjbg?autoplay=0&logo=1&hideInfos=0&start=0&syndication=134357&foreground=&highlight=&background=
				icon = "DefaultVideo.png"				
				video_url = i.attrs['src'].split('?')[0]
#				url='http://www.dailymotion.com/embed/video/x2egjbg'
				video_id = i.attrs['src'].replace('//','').split('/')[3].split('?')[0]
#				playback_url = urlresolver.resolve(video_url)
#				hosted_media_file = HostedMediaFile(url=url)
#				playback_url = hosted_media_file.resolve()
				playback_url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % video_id	
				print('dailymotion '+str(playback_url))
				parts = soup.findAll("ul", {"class" : "pagination pagination-md yuvarla"})
				print(parts)
				for part in parts:
					j = 1
					allp = part.findAll("a")
					for parturl in allp:
						if (parturl["href"]<>""):
							addDir(parturl.string,parturl["href"],3,icon)
						else:
							addDir(parturl.string,url,3,icon)
				
				
				playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
				playlist.clear()
				listitem = xbmcgui.ListItem( 'Start me', iconImage=icon, thumbnailImage="")
				listitem.setInfo( "video", { "Title": 'Start me' } )
				playlist.add( playback_url, listitem )
				xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play( playlist )
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