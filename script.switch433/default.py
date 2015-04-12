# -*- coding: utf-8 -*-
# Licence: GPL v.3 http://www.gnu.org/licenses/gpl.html

import os, sys
import xbmcgui, xbmcaddon

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path').decode(sys.getfilesystemencoding())
_addon_b1_b = _addon.getSetting( "profile1" ).decode('utf-8')
_addon_b1_n = _addon.getSetting( "name1" ).decode('utf-8')
_addon_b2_b = _addon.getSetting( "profile2" ).decode('utf-8')
_addon_b2_n = _addon.getSetting( "name2" ).decode('utf-8')
_addon_b3_b = _addon.getSetting( "profile3" ).decode('utf-8')
_addon_b3_n = _addon.getSetting( "name3" ).decode('utf-8')
_addon_b4_b = _addon.getSetting( "profile4" ).decode('utf-8')
_addon_b4_n = _addon.getSetting( "name4" ).decode('utf-8')

ACTION_PREVIOUS_MENU = 10 # Esc
ACTION_NAV_BACK = 92 # Backspace
ALIGN_CENTER = 6

background_img = os.path.join(_addon_path, 'images', 'ContentPanel.png')
button_nf_img = os.path.join(_addon_path, 'images', 'KeyboardKeyNF.png')
button_fo_img = os.path.join(_addon_path, 'images', 'KeyboardKey.png')
banana_img = os.path.join(_addon_path, 'images', 'banana.gif')
on_img = os.path.join(_addon_path, 'images', 'on.png')
off_img = os.path.join(_addon_path, 'images', 'off.png')

class MyAddon(xbmcgui.WindowDialog):

	def __init__(self):		
		background = xbmcgui.ControlImage(400, 150, 405, 305, background_img)
		self.addControl(background)

		self.set_controls()

		self.set_navigation()
		
		self.set_refresh()

	def set_controls(self):

		self.b1_btn = xbmcgui.ControlButton(505, 200, 250, 40, _addon_b1_n, focusTexture=button_fo_img,noFocusTexture=button_nf_img, alignment=ALIGN_CENTER)
		self.b2_btn = xbmcgui.ControlButton(505, 255, 250, 40, _addon_b2_n, focusTexture=button_fo_img,noFocusTexture=button_nf_img, alignment=ALIGN_CENTER)
		self.b3_btn = xbmcgui.ControlButton(505, 310, 250, 40, _addon_b3_n, focusTexture=button_fo_img,noFocusTexture=button_nf_img, alignment=ALIGN_CENTER)
		self.b4_btn = xbmcgui.ControlButton(505, 365, 250, 40, _addon_b4_n, focusTexture=button_fo_img,noFocusTexture=button_nf_img, alignment=ALIGN_CENTER)
		
		self.addControl(self.b1_btn)
		self.addControl(self.b2_btn)
		self.addControl(self.b3_btn)
		self.addControl(self.b4_btn)
	def chk_switch_on(self, switch_nr):
		if switch_nr == 1:
			return os.path.exists('/home/osmc/01110.1')
		elif switch_nr == 2:
			return os.path.exists('/home/osmc/01110.2')
		elif switch_nr == 3:
			return os.path.exists('/home/osmc/01110.3')
		elif switch_nr == 4:
			return os.path.exists('/home/osmc/01110.4')
		else:
			return false
	def set_refresh(self):
		on_pic1 = xbmcgui.ControlImage(450, 200, 50, 50, on_img)
		on_pic2 = xbmcgui.ControlImage(450, 255, 50, 50, on_img)
		on_pic3 = xbmcgui.ControlImage(450, 310, 50, 50, on_img)
		on_pic4 = xbmcgui.ControlImage(450, 365, 50, 50, on_img)

		off_pic1 = xbmcgui.ControlImage(450, 200, 50, 50, off_img)
		off_pic2 = xbmcgui.ControlImage(450, 255, 50, 50, off_img)
		off_pic3 = xbmcgui.ControlImage(450, 310, 50, 50, off_img)
		off_pic4 = xbmcgui.ControlImage(450, 365, 50, 50, off_img)


		if self.chk_switch_on(1):
			self.addControl(on_pic1)
		else:
			self.addControl(off_pic1)
		
		if self.chk_switch_on(2):
			self.addControl(on_pic2)
		else:
			self.addControl(off_pic2)
		
		if self.chk_switch_on(3):
			self.addControl(on_pic3)
		else:
			self.addControl(off_pic3)
		
		if self.chk_switch_on(4):
			self.addControl(on_pic4)
		else:
			self.addControl(off_pic4)
	def set_navigation(self):

		self.b1_btn.controlUp(self.b4_btn)
		self.b1_btn.controlDown(self.b2_btn)

		self.b2_btn.controlUp(self.b1_btn)
		self.b2_btn.controlDown(self.b3_btn)
		
		self.b3_btn.controlUp(self.b2_btn)
		self.b3_btn.controlDown(self.b4_btn)
		
		self.b4_btn.controlUp(self.b3_btn)
		self.b4_btn.controlDown(self.b1_btn)

		self.setFocus(self.b1_btn)

	def onAction(self, action):
		if action == ACTION_NAV_BACK or action == ACTION_PREVIOUS_MENU:
			self.close()

	def onControl(self, control):
		if control == self.b1_btn:
			os.system('/home/osmc/togglePower1.sh')
		elif control == self.b2_btn:
			os.system('/home/osmc/togglePower2.sh')
		elif control == self.b3_btn:
			os.system('/home/osmc/togglePower3.sh')
		elif control == self.b4_btn:
			os.system('/home/osmc/togglePower4.sh')
		self.set_refresh()
if __name__ == '__main__':
	addon = MyAddon()
	addon.doModal()
	del addon
