import dearpygui.dearpygui as dpg
import asyncio
from dbus_next.aio import MessageBus
from dbus_next import BusType

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

			# the message recieved from a player 
			if name.startswith("org.mpris.MediaPlayer2."):

				player_name = name.split('.')[-1]

				# player opened
				if new_owner != '':
					print('\nPLAYER [opened]: ', player_name, 'sender', new_owner)
					PLAYERS[player_name] = new_owner
					# add to avialable players in gui?
				
				# player closed
				else:	
					print(f"\n{player_name} has been closed [{old_owner}] ")
					PLAYERS[player_name] = None
					# stop scrobbling if initated by this player
					# lastfm.stop_scrobbler(player=player_name || player=old_owner)
					lastfm.on_track_stop()

		case "PropertiesChanged":
			try:
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
					print('\n!!! wtf', message.body)
			
			except:
				change_playback_status(message.body, message.sender)
				
async def listen_to_dbus():
	bus = await MessageBus(bus_type=BusType.SESSION).connect()
	bus.add_message_handler(message_handler)
	bus._add_match_rule("type='signal',interface='org.freedesktop.DBus.Properties',member='PropertiesChanged'")
	bus._add_match_rule("type='signal',interface='org.freedesktop.DBus',member='NameOwnerChanged'")
	await asyncio.Future()

def update_current_track(track, sender):
	
	if sender == 'spotify':
		dpg.set_value("current_track_name", track['title'])
		dpg.set_value("current_track_artist", track['artist'])
		dpg.set_value("current_track_album", track['album'])
		dpg.set_value("current_track_sender", sender)

		#add sender to list
		
	else:
		print('\n??? [def UPDATE]: sender is not spotify, but was parsed: ', track, '\tsender: ', sender)
		
			
def change_playback_status(data, sender):
	# try:
		if 'PlaybackStatus' in data[1]:
			print(f'\n[sender: {sender}]', data[1]['PlaybackStatus'])
	# except:
		else:
			print('\n[def CHNAGE PB] no pb in data[1]: ', data, '\n\t', sender)

def dbus_loop():

	dbus_thread = threading.Thread(
		target=lambda: asyncio.run(listen_to_dbus()), 
		daemon=True)
	
	dbus_thread.start()
