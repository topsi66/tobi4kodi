import sys
import xbmcgui
import xbmcplugin
import urllib2
import urllib
import re
from bs4 import BeautifulSoup

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')


def CATEGORIES():
	addDir('TV Magazin','http://fernsehkritik.tv/tv-magazin/',1,'logo.png')
                       
def INDEX(p_url):
	print('INDEX url '+p_url)
	# letzte Folge ermitteln
	req = urllib2.Request(p_url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	soup = BeautifulSoup(link)
	print(soup.original_encoding)
	folge = soup.find("div", {"class" : "col-xs-12 col-sm-7 col-md-8 col-xs-offset-0 col-sm-offset-0 col-md-offset-0 "})
	all = folge.find("a")
#		print(all)
	print('INDEX name '+all.string)
	print('INDEX href '+all.attrs['href'])

	folgenum = int(all.attrs['href'].replace('folge-',"").replace('/',""))
	epc = folgenum - int(xbmcplugin.getSetting( addon_handle,"EpisodeCount" ))
	for counter in range(folgenum,epc,-1):
		try:
			print('INDEX counter '+str(counter))
			#http://fernsehkritik.tv/folge-145/play/
			url = 'http://fernsehkritik.tv/folge-'+str(counter)+'/play/'
			print('INDEX url '+url)
			req = urllib2.Request(url)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			link=response.read()
			response.close()
			soup = BeautifulSoup(link)
			img = soup.find("video")
			folge = img.find("source", {"type" : "video/mp4"})
			print('SUB_INDEX img '+img.attrs['poster'])
			print('SUB_INDEX src '+folge.attrs['src'])
			addLink('Folge '+str(counter),folge.attrs['src'],img.attrs['poster'])
		except:
			addLink('Folge '+str(counter)+' nicht verfuegbar',"","")

				
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

elif mode==3:
	print ""+url


#INDEX('http://www.bolumizle1.com/')	
xbmcplugin.endOfDirectory(addon_handle)