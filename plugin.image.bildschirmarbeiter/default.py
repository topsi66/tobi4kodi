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
	addDir('Picdumps','http://www.bildschirmarbeiter.com/plugs/category/picdumps/',1,'logo.png')
                       
def INDEX(p_url):
	print('INDEX url '+p_url)
	req = urllib2.Request(p_url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read().decode('ascii','ignore')
	response.close()
	soup = BeautifulSoup(link)
	print(soup.original_encoding)
	
	pd = soup.findAll("a", {"class" : "plugthumb"})
	for i in pd:
		img = i.find("img")
		print('INDEX href '+i.attrs['href'])
		print('INDEX src '+'http://www.bildschirmarbeiter.com'+img.attrs['src'])
		print('INDEX alt '+img.attrs['alt'])
		addDir(img.attrs['alt'],i.attrs['href'],2,'http://www.bildschirmarbeiter.com'+img.attrs['src'])


def SUB_INDEX(p_url):
	print ('sub_index '+p_url)

	req = urllib2.Request(p_url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read().decode('ascii','ignore')
	response.close()
	soup = BeautifulSoup(link)
	print(soup.original_encoding)
	
	
	imgp = soup.findAll("img", {"class" : "image"})
	for img in imgp:	
		print('INDEX src '+img.attrs['src'])
		print('INDEX id '+img.attrs['id'])
		addLink(img.attrs['id'],img.attrs['src'],img.attrs['src'])	
	
def start_video(url):
	print ('start_video '+url)
				
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="image", infoLabels={ "Id": name })
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