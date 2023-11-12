import dearpygui.dearpygui as dpg
import asyncio
from dbus_next.aio import MessageBus
from dbus_next import BusType

import asyncio
import threading

async def listen_to_dbus():
	bus = await MessageBus(bus_type=BusType.SESSION).connect()

	def message_handler(message):
		try:
			if message.member == "NameOwnerChanged":
				name, old_owner, new_owner = message.body
				print('name changed', name)
				if name.startswith("org.mpris.MediaPlayer2."):
					if new_owner == '':
						print(f"{name} has been closed")
			else:		
				metadata_variant = message.body[1]['Metadata']
				# The actual dictionary is the value of the Variant
				metadata = metadata_variant.value
				
				album = metadata.get('xesam:album').value if 'xesam:album' in metadata else None
				artist = metadata.get('xesam:artist').value[0] if 'xesam:artist' in metadata and metadata.get('xesam:artist').value else None
				title = metadata.get('xesam:title').value if 'xesam:title' in metadata else None

				data = {
					'artist': artist,
					'title': title,
					'album': album
				}
				update_current_track(data)
				print('sender:', message.sender)

			
		except:
			update_current_track(message.body, message.sender)
		
	bus.add_message_handler(message_handler)
	# bus._add_match_rule("type='signal'")
	bus._add_match_rule("type='signal',interface='org.freedesktop.DBus.Properties',member='PropertiesChanged'")
	bus._add_match_rule("type='signal',interface='org.freedesktop.DBus',member='NameOwnerChanged'")

	await asyncio.Future()

def update_current_track(track, sender):
	
	# useless check
	# if dpg.does_item_exist("dbus_text"):
	# try:
		dpg.set_value("current_track_name", track['title'])
		dpg.set_value("current_track_artist", track['artist'])
		dpg.set_value("current_track_album", track['album'])

		# if 
		# dpg.set_value("current_track_sender", sender)
	# except:
	# 	print(track)
			
	


def dbus_loop():

	dbus_thread = threading.Thread(
		target=lambda: asyncio.run(listen_to_dbus()), 
		daemon=True)
	
	dbus_thread.start()
