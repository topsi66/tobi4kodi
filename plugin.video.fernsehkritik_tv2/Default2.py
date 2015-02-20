 import xbmc
 import xbmcplugin
 import xbmcgui
 import xbmcaddon
 import os

 xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url='http://www.nasa.gov/multimedia/nasatv/NTV-Public-IPS.m3u8',listitem=xbmcgui.ListItem('Play'))
 xbmcplugin.endOfDirectory(int(sys.argv[1]))