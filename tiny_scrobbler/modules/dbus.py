# import dearpygui.dearpygui as dpg
import asyncio
from dbus_next.aio import MessageBus
from dbus_next import BusType
from gui import update_track, switch_play_icon

import asyncio
import threading

from last import lastfm

# 'player_name' : sender
# if player is not active, sender is empty
PLAYERS = {}
CURRENT_PLAYER = None
# SEPARETE TO LIST OF AVIALABLE PLAYERS AND CHOSEN PLAYERS

get_player_name =  lambda x : [k for k,v in PLAYERS.items() if v == x][0]

	
def message_handler(message):
	match message.member:
		case "NameOwnerChanged":
			name, old_owner, new_owner = message.body # print('name changed', name, 'old_owner: ', old_owner, 'new_owner:',new_owner)
			
			if name.startswith("org.mpris.MediaPlayer2."):   #the message recieved from a player 

				player_name = name.split('.')[-1]
				
				if new_owner != '':	  #player opened
					# print('\nPLAYER [opened]: ', player_name, 'sender', new_owner)
					PLAYERS[player_name] = new_owner
					# add to avialable players in gui?
				
				else:	# player closed
					# print(f"\n{player_name} has been closed [{old_owner}] ")
					PLAYERS[player_name] = None
					# stop scrobbling if initated by this player
					# lastfm.stop_scrobbler(player=player_name || player=old_owner)
					lastfm.on_track_stop()

		case "PropertiesChanged": #probably song changed
			if 'Metadata' in message.body[1]:
				# ??? must be only fair for spotify messages
				metadata_variant = message.body[1]['Metadata']
				
				metadata = metadata_variant.value

				if metadata.get('xesam:url').value.split('.')[1] == 'spotify':
					album = metadata.get('xesam:album').value 
					artist = metadata.get('xesam:artist').value[0]
					title = metadata.get('xesam:title').value
					# album = metadata.get('xesam:album').value if 'xesam:album' in metadata else None
					# artist = metadata.get('xesam:artist').value[0] if 'xesam:artist' in metadata and metadata.get('xesam:artist').value else None
					# title = metadata.get('xesam:title').value if 'xesam:title' in metadata else None
					# url = metadata.get('xesam:url').value if 'xesam:url' in metadata else None
					data = {
						'artist': artist,
						'title': title,
						'album': album
					}
					# print('\n',message.body)	
					update_current_track(data, 'spotify')
				else:
					
					print('!!! unknown player', message.body)
					# get_player_identity(message.sender)
			
			else: # no metadata in message
				print(' PROBably playback status',)
				change_playback_status(message.body, message.sender)
				
async def listen_to_dbus():
	bus = await MessageBus(bus_type=BusType.SESSION).connect()
	bus.add_message_handler(message_handler)
	bus._add_match_rule("type='signal',interface='org.freedesktop.DBus.Properties',member='PropertiesChanged'")
	bus._add_match_rule("type='signal',interface='org.freedesktop.DBus',member='NameOwnerChanged'")
	await asyncio.Future()

def update_current_track(track, sender):
	print('\n[def UPDATE_CURRENT_TRACK]: ', track, '\tsender: ', sender)
	
	if sender == 'spotify':

		update_track(track, 'spotify')
		lastfm.on_new_track(track)

		#add sender to list
		
	else:
		print('\n??? [def UPDATE]: sender is not spotify, but was parsed: ', track, '\tsender: ', sender)
		
			
def change_playback_status(data, sender):
	if 'PlaybackStatus' in data[1]:
		status = data[1]['PlaybackStatus'].value
		print(f'[sender: {sender}]', status)
		switch_play_icon(status == 'Playing')
		lastfm.update_playnow(status == 'Playing')
		
	else:
		# not a playback status
		print('\n[def CHNAGE PB] no pb in data[1]: ', data, '\n\t', sender)

def dbus_loop():

	dbus_thread = threading.Thread(
		target=lambda: asyncio.run(listen_to_dbus()), 
		daemon=True)
	
	dbus_thread.start()
