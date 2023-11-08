#!/usr/bin/env python3
import dearpygui.dearpygui as dpg
from last import lastfm
from window import W
import gui as gui

dpg.create_context()

gui.basic_setup()

def login():
	# add login link in paratheses?
	W.set_status('authorizing with browser...')
	lastfm.authorize()
	lastfm.get_sk()    

	global main_window, login_window
	dpg.hide_item(login_window)
	W.hide_status()
	gui.load_main_window( data = lastfm.get_info())
	dpg.show_item(main_window)

def logout():
	W.set_status('logging out...')
	lastfm.logout()

	global main_window, login_window
	dpg.hide_item(main_window)
	W.hide_status()
	dpg.configure_item('header', show=False)
	dpg.show_item(login_window)




# Initialize all stages
with dpg.window(tag='primary window'):
	login_window = gui.login_window(login, lastfm.keys_are_valid)
	main_window = gui.main_window(logout_func = logout )

#user is logged in
if lastfm.username:
	gui.load_main_window( data = lastfm.get_info())
	dpg.show_item(main_window)
	# main_window = gui.main_window( data = lastfm.get_info(),
	# 							   logout_func = lastfm.logout )
else:
	dpg.show_item(login_window)
	if not lastfm.keys_are_valid:
		W.set_status(text='Invalid API keys in config.py or config.json', error=True)
	

# with dpg.window(tag='primary window'):

# 	#user is logged in
# 	if lastfm.username:
# 		gui.main_window( data = lastfm.get_info(),
# 						 logout_func = lastfm.logout )
# 	else:
# 		gui.login_window(login, lastfm.keys_are_valid)
# 		if not lastfm.keys_are_valid:
# 			W.set_status(text='Invalid API keys in config.py or config.json', error=True)
# 		# else:
# 		# 	print('keys are valid')
# 		# 	if lastfm.username:
# 		# 		try: 
# 		# 			print('trying to log in')
# 		# 			gui.main_window( data = lastfm.get_info(),
# 		# 				logout_func = lastfm.logout )
# 		# 		except:
# 		# 			pass


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('primary window', True)
dpg.start_dearpygui()
dpg.destroy_context()