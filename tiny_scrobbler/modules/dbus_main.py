import asyncio
import dbus

async def main():
    # Get the asynchronous generator
    async_gen = await dbus.monitor_properties_changes()

    # Asynchronously iterate over the generator to get data
    async for data in async_gen:
        # Do something with the data
        print(data)

if __name__ == "__main__":
    dbus.ON_MONITOR = True
    asyncio.run(main())

import asyncio
asyncio.get_event_loop().run_until_complete(main())