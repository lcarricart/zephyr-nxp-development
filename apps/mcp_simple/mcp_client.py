import asyncio

from fastmcp import Client

async def main():
    # Connect and initialize the MCP session; allow time for the delayed tool.
    async with Client('http://169.254.176.190:8080/mcp') as client:
        # Discover the tools exposed by the Zephyr server (MCP tools/list).
        tools = await client.list_tools()
        print('Available tools:')
        for tool in tools:
            print(f'  - {tool.name}')

        # Turn the LED off, then back on.
        result = await client.call_tool('led_control', {'action': 'off'})
        print('\nLED off:', result)
        await asyncio.sleep(0.5)

        result = await client.call_tool('led_control', {'action': 'on'})
        print('LED on:', result)

        # This tool waits a certain time until returning its response
        result = await client.call_tool('delayed_response', {'message': 'test'})
        print('Delayed response:', result)

asyncio.run(main())
