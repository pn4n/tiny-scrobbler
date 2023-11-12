from dbus_next.aio import MessageBus
from dbus_next import BusType
ON_MONITOR = False

async def monitor_properties_changes():
	bus = await MessageBus(bus_type=BusType.SESSION).connect()

	bus._add_match_rule("type='signal',interface='org.freedesktop.DBus.Properties',member='PropertiesChanged'")

	async def properties_changed_handler(message):
		# while ON_MONITOR:
			# message = await bus.wait_for_message()
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
				return data  # Yield the extracted data
			except:
				pass

	return properties_changed_handler()

	