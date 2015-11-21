import sys
import xbmcgui
import xbmcplugin
import urllib2
import urllib
import re
import urlresolver
import json
from bs4 import BeautifulSoup

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'movies')


def CATEGORIES():
	addDir('Podcast','https://www.ndr.de/fernsehen/sendungen/extra_3/video-podcast/index.html',1,'icon.png')
                       
def INDEX(p_url):
	print('INDEX url '+p_url)
	req = urllib2.Request(p_url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	soup = BeautifulSoup(link)
#	print(soup)
	#Naechste Seite ermitteln
	pagi = soup.find("div", {"class" : "pagination"})
	pag_weiter = pagi.find("a", {"title" : "weiter"})
	if pag_weiter != None:
		print('Weiter: '+pag_weiter.attrs['href'])
		addDir('Naechste Seite','https://www.ndr.de'+pag_weiter.attrs['href'],1,'icon.png')
	
	#Folgen ermitteln 
	serien = soup.findAll("div", {"class" : "teaserpadding"})
	for i in serien:
		folgen = all = i.find("a")
		#Laden der Sub Websites
		r_url = folgen.attrs['href']
		if r_url.find('daserste.ndr.de') > 0:
			r_url = 'false'
		elif r_url[0] == '/':
			r_url = 'https://www.ndr.de'+r_url
		print('URL :'+r_url)
		if r_url != 'false':
			req = urllib2.Request(r_url)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			episode=response.read()
			response.close()
			soup_ep = BeautifulSoup(episode)
			content_url = soup_ep.find("span", {"itemprop" : "contentUrl"})
			content_img = soup_ep.find("span", {"itemprop" : "thumbnailUrl"})
			addLink(folgen.string,content_url.attrs['content'],content_img.attrs['content'])
		
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

#INDEX('http://www.bolumizle1.com/')	
xbmcplugin.endOfDirectory(addon_handle)