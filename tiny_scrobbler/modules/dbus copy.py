from dbus_next.aio import MessageBus
from dbus_next import BusType, Message

async def main():
	bus = await MessageBus(bus_type=BusType.SESSION).connect()

	bus._add_match_rule("type='signal',interface='org.freedesktop.DBus.Properties',member='PropertiesChanged'")

	def on_properties_changed(message: Message):
		try:
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
			yield data
		except:
			pass
		# print(f"Sender: {message.sender}")
		# print(f"Body: {message.body}")
		# print('========\n')

		# print('sender', message.sender)
		# print('body', message.body)

	bus.add_message_handler(on_properties_changed)


	await bus.wait_for_disconnect()

	